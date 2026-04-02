<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&pause=1000&color=76e033&center=true&vCenter=true&width=700&lines=Mr-SxR+Range+Share+Bot;Telegram+OTP+Range+Forwarder+%7C+Mr-SxR" alt="Typing SVG" />

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)
![Open Source](https://img.shields.io/badge/Open%20Source-✓-76e033?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## 📌 About

**Mr-SxR Range Share Bot** is an open-source Python automation tool developed under the **Mr-SxR** brand. It continuously polls a target dashboard API, detects new incoming logs (filtered by platform — Facebook & WhatsApp), and instantly forwards them to a Telegram group or channel via bot.

Key highlights:
- **Multi-token rotation** — Distribute Telegram API rate limits across multiple bots automatically
- **Concurrent delivery** — Uses Python ThreadPoolExecutor for non-blocking message dispatch
- **Smart deduplication** — Tracks already-sent log IDs to avoid duplicate messages
- **Inline Copy Button** — Each forwarded message includes a one-tap button to copy the range value

---

## ⚙️ Installation

```bash
git clone https://github.com/Mr-SxR/Xmnit-range-forwarder-bot.git
cd Xmnit-range-forwarder-bot
pip install -r requirements.txt
```

---

## 🔧 Configuration

Open `config.json` and fill in your values:

```json
{
    "telegram": {
        "bot_tokens": [
            "YOUR_BOT_TOKEN_1",
            "YOUR_BOT_TOKEN_2",
            "YOUR_BOT_TOKEN_3"
        ],
        "chat_id": "YOUR_CHAT_ID"
    },
    "authentication": {
        "auth_token": "YOUR_AUTH_TOKEN",
        "cf_clearance": "YOUR_CF_CLEARANCE"
    }
}
```

---

## 📖 Config Fields Explained

### 🤖 Telegram

| Field | Description |
|-------|-------------|
| `bot_tokens` | List of Telegram bot tokens. One is enough, but multiple tokens allow automatic rotation to avoid rate limits. Every 10 messages the bot switches to the next token in the list. |
| `chat_id` | The Telegram group or channel ID where messages will be forwarded. For groups/channels, it starts with `-100`. |

**How to get a bot token:**
1. Open Telegram → search **@BotFather**
2. Send `/newbot` and follow the steps
3. Copy the token and paste it into `bot_tokens`

---

### 🔐 Authentication

These two values come from your browser session on the target dashboard website. You need to be logged in to retrieve them.

| Field | Description |
|-------|-------------|
| `auth_token` | Your session authentication token from the website |
| `cf_clearance` | Cloudflare clearance cookie that proves you passed the browser challenge |

**How to get these values:**

1. Open the target website in **Google Chrome** and log in
2. Press `F12` to open DevTools → go to **Network** tab
3. Refresh the page and click on any API request to the dashboard
4. Go to **Headers** → scroll down to **Request Headers**
5. Find and copy:
   - `mauthtoken` → paste as `auth_token`
   - `cf_clearance` (under Cookies) → paste as `cf_clearance`

> ⚠️ These values expire periodically. If the bot stops receiving data, repeat the steps above to get fresh values.

---

## ▶️ Usage

```bash
python main.py
```

The bot will start polling immediately. When new logs arrive, they are forwarded to your Telegram chat in this format:

```
🌍 Country: Bangladesh
📱 Service: Facebook
💬 Message:
Your OTP code is XXXXXX
[Copy Range]
```

---

## 🔁 Multi-Token Rotation

If you add multiple bot tokens, the bot automatically rotates between them every **10 messages**. This helps avoid Telegram's rate limiting when forwarding large volumes of messages.

```json
"bot_tokens": [
    "TOKEN_1",
    "TOKEN_2",
    "TOKEN_3"
]
```

You can add as many tokens as you need. One token is also perfectly fine for low-volume usage.

---

## 📋 Requirements

```
requests
flask
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📬 Contact

[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/sifathub)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/+8801858094178)
[![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/sifathub)

---

<div align="center">

*Developed & Open-Sourced by **[Mr-SxR](https://github.com/mr-sxr)** — Speciality & Reliability*

</div>
