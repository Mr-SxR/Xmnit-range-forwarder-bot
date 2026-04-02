"""
Project: Mr-SxR Range share Bot
Developer: Masudur Rahman Sifat
Brand / Alias: Mr-SxR
"""

import os
import requests
import time
import json
import concurrent.futures
import sys

# Force unbuffered output for standard streams (useful for remote deployments like Render/Heroku)
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

CONFIG_FILE = 'config.json'

def load_config():
    #Load configuration variables from the JSON file.
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: '{CONFIG_FILE}' not found! Please create it using 'config_example.json' as a template.")
        sys.exit(1)
        
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{CONFIG_FILE}' is not a valid JSON file.")
        sys.exit(1)

def snd_tle_msg(message, bot_token, chat_id, reply_markup=None, count=0):
    # Sends a formatted message to a Telegram chat using a specific bot token.
    # Implements a simple retry mechanism for failed requests.
    # Safety catch: Stop retrying after 3 unsuccessful attempts
    if count >= 3:
        print(f"Failed to send message after {count} attempts. Giving up on this payload.")
        return

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    # Add optional inline keyboard wrapper if provided
    if reply_markup:
        payload['reply_markup'] = reply_markup

    try:
        response = requests.post(telegram_url, data=payload, timeout=10)
        response.raise_for_status()
        resp_data = response.json()
        
        if resp_data.get('ok'):
            print("Telegram message dispatched successfully.")
        else:
            print(f"Telegram API rejected the message (Attempt {count + 1}). Retrying...")
            snd_tle_msg(message, bot_token, chat_id, reply_markup, count + 1)

    except requests.exceptions.RequestException as e:
        print(f"Network error while sending message via Telegram: {e} | Attempt: {count + 1}")
        time.sleep(1) # Brief pause before attempting a retry
        snd_tle_msg(message, bot_token, chat_id, reply_markup, count + 1)

def main():
    # 1. Load sensitive configuration data dynamically
    config = load_config()
    
    telegram_config = config.get('telegram', {})
    auth_config = config.get('authentication', {})
    
    bot_tokens = telegram_config.get('bot_tokens', [])
    chat_id = telegram_config.get('chat_id')
    auth_token = auth_config.get('auth_token')
    cf_clearance = auth_config.get('cf_clearance')
    
    # Validate critical configurations before proceeding
    if not bot_tokens or not chat_id or not auth_token:
        print("Error: Missing required config keys (bot_tokens, chat_id, or auth_token).")
        sys.exit(1)

    # 2. Set up session cookies needed to authorize requests
    cookies = {
        'cf_clearance': cf_clearance,
        'mauthtoken': auth_token,
    }

    # API request headers mimicking a legitimate Chrome Windows session
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-BD,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'mauthtoken': auth_token,
        'priority': 'u=1, i',
        'referer': 'https://x.mnitnetwork.com/mdashboard/console',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    }
    
    seen_ids = set()
    total_sent_count = 0
    
    # 3. Initialize ThreadPoolExecutor for concurrent message delivery
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    
    print("Bot initialized successfully. Listening for incoming messages...")

    while True:
        try:
            # Poll the target API for new data chunks
            response = requests.get(
                'https://x.mnitnetwork.com/mapi/v1/mdashboard/console/info',
                cookies=cookies,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            logs = data.get('data', {}).get('logs', [])
            
            new_logs = []
            
            # Extract logs that haven't been processed yet
            for log in logs:
                log_id = log.get('id')
                if log_id not in seen_ids:
                    new_logs.append(log)
                    seen_ids.add(log_id)
            
            if new_logs:
                print(f"[{time.strftime('%X')}] Found {len(new_logs)} new log(s). Sending...")
                
                # Process oldest logs first by reading the log array in reverse
                for log in reversed(new_logs):
                    app_name = log.get('app_name', 'Unknown')
                    
                    # Target specfic apps to reduce spam
                    if app_name.lower() not in ['facebook', 'whatsapp']:
                        # print(f"--- Suppressed unsupported platform: {app_name} ---") # Optional debugging
                        continue
                        
                    # Clean up the SMS body to avoid breaking HTML Telegram parsing
                    sms_body = log.get('sms', '')
                    sms_body = sms_body.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
                    
                    rng = log.get('range', '')
                    country = log.get('country', 'Unknown')

                    # 4. Construct the outgoing Telegram template
                    msg = (
                        f"<b>🌍 Country:</b> {country}\n"
                        f"<b>📱 Service:</b> {app_name}\n"
                        f"<b>💬 Message:</b>\n"
                        f"<code>{sms_body}</code>\n"
                    )
                    
                    # 5. Add an interactive inline button for UX optimization (Fast copying)
                    reply_markup = json.dumps({
                        "inline_keyboard": [[
                            {"text": "Copy Range", "copy_text": {"text": rng}}
                        ]]
                    })
                    
                    # 6. Smoothly rotate between tokens to distribute rate limits over multiple bots
                    cycle_index = (total_sent_count // 10) % len(bot_tokens)
                    current_bot_token = bot_tokens[cycle_index]
                    
                    # Delegate the network I/O heavily bound task to background thread pools
                    executor.submit(snd_tle_msg, msg, current_bot_token, chat_id, reply_markup)
                    total_sent_count += 1
            else:
                pass # Silent pass if no logs are there to keep stdout clean

        except requests.exceptions.HTTPError as he:
            print(f"HTTP error during log fetch: {he}")
        except requests.exceptions.RequestException as e:
            print(f"Network error during log fetch: {e}")
        except Exception as e:
            print(f"Unexpected system error: {e}")
            
        # Cooldown timer to balance load on endpoint servers
        time.sleep(5)

if __name__ == "__main__":
    main()

