# 🛡 FileGuard — Telegram Edition Setup

Get alerts on Telegram and remotely delete files — 3 steps, 10 minutes.

---

## Step 1 — Create Your Telegram Bot (2 min)

1. Open Telegram → search for **@BotFather**
2. Send: `/newbot`
3. Choose a name: e.g. `FileGuard Bot`
4. Choose a username: e.g. `myfileguard_bot`
5. Copy the **TOKEN** it gives you (looks like `1234567890:ABCdef...`)

### Get your Chat ID:
1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It replies with your **Chat ID** (a number like `987654321`)

---

## Step 2 — Configure the Script (1 min)

Open `fileguard_telegram.py` and edit these 3 lines at the top:

```python
TELEGRAM_TOKEN   = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"  # ← paste your token
TELEGRAM_CHAT_ID = "987654321"                                # ← paste your chat ID
DEVICE_NAME      = "ZERO_BOOK_13"                              # ← give your PC a name
```

---

## Step 3A — Run Manually (test first)

```batch
# Install dependencies
pip install -r requirements.txt

# Run the script
python fileguard_telegram.py
```

You should get a Telegram message saying **"FileGuard Started"**.
Plug in a USB drive and copy a file — you'll get an alert instantly!

---

## Step 3B — Install as Background Service (permanent)

Once tested, run this to make it start automatically with Windows:

```
Right-click install_service.bat → Run as Administrator
```

That's it. FileGuard will:
- ✅ Run silently in the background
- ✅ Auto-start every time Windows boots
- ✅ Keep running even when no user is logged in
- ✅ Log everything to `fileguard.log`

---

## How to Use from Telegram

When someone copies a file to a USB, you get this message:

```
🚨 FILE TRANSFER DETECTED
━━━━━━━━━━━━━━━━━━━━━
📋 Event: COPIED to USB
📄 File: secret_data.xlsx
📦 Size: 2.4 MB
💾 Drive: E:\
🕐 Time: 10:42:15
🖥 PC: My Home PC
━━━━━━━━━━━━━━━━━━━━━
🆔 Alert ID: a3f7b2c1

[🗑 DELETE FILE]  [✅ Allow]
```

Tap **DELETE FILE** → file is permanently removed from the USB.
Tap **Allow** → transfer is marked safe.

### Other commands:
| Command | Action |
|---------|--------|
| `/status` | Check if agent is running |
| `/list` | See all pending alerts |
| `/help` | Show all commands |

---

## Manage the Service

```batch
sc stop FileGuard       # Stop it
sc start FileGuard      # Start it
sc query FileGuard      # Check status
type fileguard.log      # View logs
```

To uninstall:
```batch
nssm remove FileGuard confirm
```

---

## Troubleshooting

**No Telegram message on startup?**
- Double-check your TOKEN and CHAT_ID
- Make sure Python can reach the internet

**Not detecting USB files?**
- Run as Administrator (or the service runs as SYSTEM which has full access)
- Check `fileguard.log` for errors

**Delete button not working?**
- The script must be running on the PC at the time you press Delete
- Check `fileguard.log` for permission errors
