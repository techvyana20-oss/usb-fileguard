# FileGuard — Telegram Edition 🛡

A powerful USB monitoring tool built with Python that sends real-time Telegram alerts whenever files are copied or moved to a USB drive. You can even remotely delete suspicious files directly from Telegram.

---

# 👨‍💻 Author

**Bhavya Jain**

# 📺 Channel

**TechVyana2.0**

---

# ⚠️ Educational Purpose Only

This project is made only for educational and learning purposes.

The purpose of this project is:
- Learning Python automation
- Understanding USB monitoring
- Learning Telegram Bot API
- Learning file system monitoring
- Understanding cybersecurity concepts

The author is not responsible for any misuse of this tool.

---

# ✨ Features

- 🔔 Real-time Telegram alerts
- 🖥 USB drive monitoring
- 🗑 Remote file delete system
- 🔒 USB lockdown mode
- 📋 Telegram control commands
- ⚡ Beautiful Tkinter setup UI
- 💾 Auto-save configuration
- 🧠 Smart alert system
- 📁 File extension protection
- 🔄 Auto USB detection

---

# 📦 Installation

## Step 1 — Install Python

Download Python from:

https://www.python.org/downloads/

While installing, enable:

```bash
Add Python to PATH
```

---

## Step 2 — Install Requirements

Open CMD inside the project folder and run:

```bash
pip install -r requirements.txt
```

---

# 📄 requirements.txt

```txt
watchdog>=6.0.0
psutil==5.9.8
pywin32==311
requests==2.31.0
```

---

# 📚 Why These Libraries Are Used

## 1️⃣ watchdog

```bash
pip install watchdog
```

### Why we used it:

`watchdog` is used to monitor files and folders in real-time.

It detects:
- File copy
- File move
- File creation

Without this library, the program cannot detect USB file activity.

---

## 2️⃣ psutil

```bash
pip install psutil
```

### Why we used it:

`psutil` helps detect connected USB drives and system information.

It is used for:
- Detecting removable drives
- Monitoring system devices
- Reading disk partitions

---

## 3️⃣ pywin32

```bash
pip install pywin32
```

### Why we used it:

`pywin32` allows Python to communicate with Windows system functions.

It is used for:
- USB drive control
- Windows registry access
- Write protection (Lockdown mode)

This project mainly uses it for Windows-level USB control.

---

## 4️⃣ requests

```bash
pip install requests
```

### Why we used it:

`requests` is used to connect with the Telegram Bot API.

It helps:
- Send Telegram messages
- Receive commands
- Delete file requests
- Handle Telegram buttons

---

# 🚀 How To Run

## Run the Script

```bash
python fileguard_telegram.py
```

---

# 🤖 Telegram Bot Setup

## Create Bot

1. Open Telegram
2. Search for **@BotFather**
3. Send:

```txt
/newbot
```

4. Copy your Bot Token

---

## Get Chat ID

1. Search **@userinfobot**
2. Send any message
3. Copy your Chat ID

---

# 🛠 Setup Screen

When you run the script, a setup window will open.

Enter:
- Telegram Bot Token
- Telegram Chat ID
- Device Name

Then click:

```txt
Save & Start FileGuard
```

---

# 💬 Telegram Commands

| Command | Work |
|---|---|
| `/status` | Check FileGuard status |
| `/list` | Show pending alerts |
| `/help` | Show all commands |
| `/lockdown` | Enable USB lockdown |
| `/unlock` | Disable lockdown |
| `/delete_ID` | Delete a file |
| `/allow_ID` | Mark file safe |

---

# 🔒 Lockdown Mode

When Lockdown Mode is ON:
- USB becomes write-protected
- Copied files are instantly deleted
- Prevents unauthorized transfers

---

# 🖥 Run As Background Service

To auto-start with Windows:

Run:

```txt
install_service.bat
```

as Administrator.

---

# 📁 Project Files

| File | Purpose |
|---|---|
| `fileguard_telegram.py` | Main Python script |
| `requirements.txt` | Python dependencies |
| `install_service.bat` | Install as Windows service |
| `SETUP_TELEGRAM.md` | Telegram setup guide |

---

# 📜 License

## MIT License

Copyright (c) 2026 Bhavya Jain

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to use, copy, modify, and distribute the software for educational purposes.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

# ❤️ Credits

Created by **Bhavya Jain**

YouTube Channel: **TechVyana2.0**

---

# ⭐ Support

If you like this project:
- Subscribe to TechVyana2.0
- Share the project
- Learn and build more projects 🚀

