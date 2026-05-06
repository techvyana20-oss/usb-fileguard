"""
FileGuard — Telegram Edition  v2.4  (Python 3.13 compatible)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Author  : Bhavya Jain
  Channel : Techvyana2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEW in v2.4
───────────
  🖥  Beautiful Tkinter Setup UI — Token, Chat ID, Device Name
      entered through a styled dark GUI on first run.
  ⚡  Live "Test Connection" button validates token instantly.
  💾  Config auto-saved to fileguard_config.json.
  🔄  Run with --setup to force re-configuration any time.

v2.3 fixes
──────────
  ✅ Graceful Ctrl+C — no KeyboardInterrupt traceback.
  ✅ signal.signal() catches SIGINT/SIGTERM cleanly.
  ✅ threading.Event replaces bare sleep loop.
"""

import os, sys, json, time, hashlib, logging, threading, signal, winreg
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
from collections import OrderedDict

import psutil
import requests
import win32con
import win32file
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

# ═══════════════════════════════════════════════════════════════════
#  CONFIG FILE
# ═══════════════════════════════════════════════════════════════════

CONFIG_FILE = "fileguard_config.json"

def load_config():
    if Path(CONFIG_FILE).exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(token, chat_id, device_name):
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "TELEGRAM_TOKEN":   token,
            "TELEGRAM_CHAT_ID": chat_id,
            "DEVICE_NAME":      device_name
        }, f, indent=2)

# ═══════════════════════════════════════════════════════════════════
#  COLOUR PALETTE
# ═══════════════════════════════════════════════════════════════════

BG_DARK    = "#0d1117"
BG_CARD    = "#161b22"
BG_INPUT   = "#21262d"
ACCENT     = "#58a6ff"
ACCENT2    = "#3fb950"
WARN       = "#f85149"
GOLD       = "#e3b341"
TEXT_WHITE = "#f0f6fc"
TEXT_GREY  = "#8b949e"
TEXT_DIM   = "#484f58"
BORDER     = "#30363d"

# ═══════════════════════════════════════════════════════════════════
#  SETUP UI
# ═══════════════════════════════════════════════════════════════════

class SetupUI:
    """
    Styled dark-theme Tkinter window to collect:
      - Telegram Bot Token
      - Telegram Chat ID
      - Device / PC Name

    Author  : Bhavya Jain
    Channel : Techvyana2.0
    """

    def __init__(self):
        self.result = None

        self.root = tk.Tk()
        self.root.title("FileGuard — Setup  |  Techvyana2.0")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)

        # Centre window
        w, h = 540, 670
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Build layout ───────────────────────────────────────────────

    def _build(self):
        existing = load_config()

        # ════ HEADER BANNER ════════════════════════════════════════
        banner = tk.Frame(self.root, bg=BG_CARD)
        banner.pack(fill="x")

        # Shield icon (drawn on canvas)
        cv = tk.Canvas(banner, width=68, height=68,
                        bg=BG_CARD, highlightthickness=0)
        cv.pack(pady=(18, 2))
        self._draw_shield(cv)

        tk.Label(banner, text="FileGuard",
                 bg=BG_CARD, fg=TEXT_WHITE,
                 font=("Segoe UI", 24, "bold")).pack()

        tk.Label(banner, text="Telegram USB Monitor — First Run Setup",
                 bg=BG_CARD, fg=TEXT_GREY,
                 font=("Segoe UI", 10)).pack(pady=(0, 6))

        # Blue accent line
        tk.Frame(banner, bg=ACCENT, height=2).pack(fill="x")

        # ════ AUTHOR BAR ═══════════════════════════════════════════
        ab = tk.Frame(self.root, bg=BG_DARK)
        ab.pack(fill="x", pady=8)

        tk.Label(ab,
                 text="✦   Author : Bhavya Jain     |     Channel : Techvyana2.0   ✦",
                 bg=BG_DARK, fg=GOLD,
                 font=("Segoe UI", 9, "italic bold")).pack()

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=20)

        # ════ FORM CARD ════════════════════════════════════════════
        card = tk.Frame(self.root, bg=BG_CARD,
                        highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="x", padx=22, pady=(14, 0))

        tk.Label(card, text="  ⚙  Configuration",
                 bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 10, "bold"),
                 anchor="w").pack(fill="x", padx=6, pady=(10, 4))

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=10)

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="x", padx=16, pady=10)

        # ── Field 1 : Bot Token ────────────────────────────────────
        self._lbl(inner, "🤖  Telegram Bot Token")
        self.token_var = tk.StringVar(
            value=existing.get("TELEGRAM_TOKEN", ""))

        tok_wrap = tk.Frame(inner, bg=BG_INPUT,
                            highlightbackground=BORDER,
                            highlightthickness=1)
        tok_wrap.pack(fill="x", pady=(2, 4))

        self.token_entry = tk.Entry(
            tok_wrap, textvariable=self.token_var,
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=ACCENT,
            relief="flat",
            font=("Consolas", 10),
            show="•"
        )
        self.token_entry.pack(fill="x", padx=8, pady=7)

        # Show / hide toggle
        tog = tk.Frame(inner, bg=BG_CARD)
        tog.pack(fill="x", pady=(0, 10))
        self._show_tok = tk.BooleanVar(value=False)
        tk.Checkbutton(
            tog, text="Show token",
            variable=self._show_tok,
            command=self._toggle_token,
            bg=BG_CARD, fg=TEXT_GREY,
            activebackground=BG_CARD,
            selectcolor=BG_INPUT,
            font=("Segoe UI", 8)
        ).pack(side="left")

        # ── Field 2 : Chat ID ──────────────────────────────────────
        self._lbl(inner, "💬  Telegram Chat ID")
        self.chat_var = tk.StringVar(
            value=existing.get("TELEGRAM_CHAT_ID", ""))

        chat_wrap = tk.Frame(inner, bg=BG_INPUT,
                              highlightbackground=BORDER,
                              highlightthickness=1)
        chat_wrap.pack(fill="x", pady=(2, 4))

        tk.Entry(
            chat_wrap, textvariable=self.chat_var,
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=ACCENT,
            relief="flat",
            font=("Consolas", 10)
        ).pack(fill="x", padx=8, pady=7)

        tk.Label(inner,
                 text="  ↳ Message @userinfobot on Telegram to get your Chat ID",
                 bg=BG_CARD, fg=TEXT_GREY,
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(0, 10))

        # ── Field 3 : Device Name ──────────────────────────────────
        self._lbl(inner, "🖥  Device / PC Name")
        self.device_var = tk.StringVar(
            value=existing.get("DEVICE_NAME",
                               os.environ.get("COMPUTERNAME", "MY_PC")))

        dev_wrap = tk.Frame(inner, bg=BG_INPUT,
                             highlightbackground=BORDER,
                             highlightthickness=1)
        dev_wrap.pack(fill="x", pady=(2, 4))

        tk.Entry(
            dev_wrap, textvariable=self.device_var,
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=ACCENT,
            relief="flat",
            font=("Consolas", 10)
        ).pack(fill="x", padx=8, pady=7)

        tk.Label(inner,
                 text="  ↳ Label shown in every Telegram alert",
                 bg=BG_CARD, fg=TEXT_GREY,
                 font=("Segoe UI", 8)).pack(anchor="w")

        # ════ STATUS LABEL ═════════════════════════════════════════
        self.status_var = tk.StringVar(value="")
        self.status_lbl = tk.Label(
            self.root, textvariable=self.status_var,
            bg=BG_DARK, fg=TEXT_GREY,
            font=("Segoe UI", 9),
            wraplength=490, justify="center"
        )
        self.status_lbl.pack(pady=(12, 0), padx=22)

        # ════ BUTTONS ══════════════════════════════════════════════
        btn_area = tk.Frame(self.root, bg=BG_DARK)
        btn_area.pack(fill="x", padx=22, pady=(10, 0))

        self.test_btn = self._btn(
            btn_area,
            "⚡  Test Connection",
            ACCENT, "#1f6feb",
            self._test_connection
        )
        self.test_btn.pack(fill="x", pady=(0, 8))

        self.save_btn = self._btn(
            btn_area,
            "🚀  Save & Start FileGuard",
            ACCENT2, "#238636",
            self._save_and_start
        )
        self.save_btn.pack(fill="x")

        # ════ FOOTER ═══════════════════════════════════════════════
        tk.Frame(self.root, bg=BORDER, height=1).pack(
            fill="x", padx=20, pady=(16, 0))

        tk.Label(self.root,
                 text="FileGuard v2.4   •   Techvyana2.0   •   Bhavya Jain",
                 bg=BG_DARK, fg=TEXT_DIM,
                 font=("Segoe UI", 8)).pack(pady=8)

    # ── Widget helpers ─────────────────────────────────────────────

    def _draw_shield(self, cv):
        pts = [34, 6, 60, 18, 60, 40, 34, 62, 8, 40, 8, 18]
        cv.create_polygon(pts, fill=ACCENT, outline=BORDER,
                           width=1.5, smooth=True)
        cv.create_line(20, 34, 30, 46, 48, 22,
                       fill="white", width=3.5,
                       capstyle="round", joinstyle="round")

    def _lbl(self, parent, text):
        tk.Label(parent, text=text,
                 bg=BG_CARD, fg=TEXT_WHITE,
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(fill="x", pady=(4, 0))

    def _btn(self, parent, text, fg, hover, cmd):
        b = tk.Button(
            parent, text=text,
            bg=BG_INPUT, fg=fg,
            activebackground=BG_CARD,
            activeforeground=fg,
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            pady=10, command=cmd,
            highlightbackground=fg,
            highlightthickness=1
        )
        b.bind("<Enter>", lambda e: b.configure(bg=hover, fg="white"))
        b.bind("<Leave>", lambda e: b.configure(bg=BG_INPUT, fg=fg))
        return b

    def _set_status(self, msg, color=TEXT_GREY):
        self.status_var.set(msg)
        self.status_lbl.configure(fg=color)
        self.root.update_idletasks()

    def _toggle_token(self):
        self.token_entry.configure(
            show="" if self._show_tok.get() else "•")

    # ── Actions ────────────────────────────────────────────────────

    def _test_connection(self):
        token   = self.token_var.get().strip()
        chat_id = self.chat_var.get().strip()

        if not token:
            self._set_status("⚠️  Please enter a Bot Token first.", WARN)
            return

        self._set_status("🔄  Testing connection…", ACCENT)
        self.test_btn.configure(state="disabled")
        self.root.update_idletasks()

        def _worker():
            try:
                r = requests.get(
                    f"https://api.telegram.org/bot{token}/getMe",
                    timeout=8)
                data = r.json()
                if not r.ok or not data.get("ok"):
                    self.root.after(0, self._set_status,
                        f"❌  Invalid token: {data.get('description','Unknown error')}",
                        WARN)
                    return

                bot = data["result"].get("username", "Unknown")

                if chat_id:
                    r2 = requests.post(
                        f"https://api.telegram.org/bot{token}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": (
                                "✅ <b>FileGuard — Connection Test OK</b>\n"
                                "🛡 Bot is live and ready.\n"
                                "👤 Bhavya Jain | Techvyana2.0"
                            ),
                            "parse_mode": "HTML"
                        },
                        timeout=8
                    )
                    if r2.ok:
                        msg = f"✅  @{bot} — Test message sent to Telegram!"
                        clr = ACCENT2
                    else:
                        err = r2.json().get("description", "Unknown")
                        msg = f"⚠️  Bot OK (@{bot}) but Chat ID failed: {err}"
                        clr = GOLD
                else:
                    msg = f"✅  Token valid: @{bot}  (add Chat ID to send a test)"
                    clr = ACCENT2

                self.root.after(0, self._set_status, msg, clr)

            except requests.exceptions.ConnectionError:
                self.root.after(0, self._set_status,
                    "❌  No internet connection.", WARN)
            except Exception as exc:
                self.root.after(0, self._set_status,
                    f"❌  Error: {exc}", WARN)
            finally:
                self.root.after(
                    0, lambda: self.test_btn.configure(state="normal"))

        threading.Thread(target=_worker, daemon=True).start()

    def _save_and_start(self):
        token       = self.token_var.get().strip()
        chat_id     = self.chat_var.get().strip()
        device_name = self.device_var.get().strip()

        # Validation
        if not token:
            self._set_status("⚠️  Bot Token is required.", WARN); return
        if not chat_id:
            self._set_status("⚠️  Chat ID is required.", WARN); return
        if not device_name:
            self._set_status("⚠️  Device Name is required.", WARN); return
        if ":" not in token or len(token) < 30:
            self._set_status(
                "⚠️  Token format looks wrong  (e.g. 123456789:ABCdef…)", WARN)
            return
        if not chat_id.lstrip("-").isdigit():
            self._set_status(
                "⚠️  Chat ID must be numeric  (e.g. 5422402700)", WARN)
            return

        save_config(token, chat_id, device_name)
        self._set_status("💾  Config saved — launching FileGuard…", ACCENT2)
        self.root.update_idletasks()

        self.result = (token, chat_id, device_name)
        self.root.after(700, self.root.destroy)

    def _on_close(self):
        if messagebox.askyesno("Exit",
                               "Cancel setup and exit FileGuard?",
                               parent=self.root):
            self.root.destroy()
            sys.exit(0)

    def run(self):
        """Show window; return (token, chat_id, device_name) or sys.exit."""
        self.root.mainloop()
        if self.result is None:
            sys.exit(0)
        return self.result


# ── Config loader ──────────────────────────────────────────────────

def get_config():
    force = "--setup" in sys.argv or "--reconfigure" in sys.argv
    cfg   = load_config()
    if (not force
            and cfg.get("TELEGRAM_TOKEN")
            and cfg.get("TELEGRAM_CHAT_ID")):
        return (cfg["TELEGRAM_TOKEN"],
                cfg["TELEGRAM_CHAT_ID"],
                cfg.get("DEVICE_NAME", "MY_PC"))
    return SetupUI().run()


# ═══════════════════════════════════════════════════════════════════
#  RUNTIME GLOBALS  (set after UI)
# ═══════════════════════════════════════════════════════════════════

TELEGRAM_TOKEN   = ""
TELEGRAM_CHAT_ID = ""
DEVICE_NAME      = ""

WATCH_ALL_FILES   = True
ALERT_COOLDOWN    = 1
MAX_ALERTS_MEMORY = 50

PROTECTED_EXTENSIONS = {
    ".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".xls",
    ".txt", ".csv", ".sql", ".py", ".js", ".ts",
    ".zip", ".rar", ".7z",
    ".jpg", ".jpeg", ".png", ".gif",
    ".mp4", ".mov", ".avi", ".mkv",
    ".pem", ".key", ".env", ".config"
}

# ═══════════════════════════════════════════════════════════════════
#  GLOBAL STATE
# ═══════════════════════════════════════════════════════════════════

_lockdown_lock   = threading.Lock()
_lockdown_active = True
_shutting_down   = False

def is_lockdown():
    with _lockdown_lock:
        return _lockdown_active

def set_lockdown(val: bool):
    global _lockdown_active
    with _lockdown_lock:
        _lockdown_active = val

# ═══════════════════════════════════════════════════════════════════
#  DRIVE BLOCKER
# ═══════════════════════════════════════════════════════════════════

class DriveBlocker:
    _REG_PATH = r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
    _REG_KEY  = "WriteProtect"

    @classmethod
    def block(cls):
        try:
            key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                     cls._REG_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, cls._REG_KEY, 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            return True, None
        except PermissionError:
            return False, "permission_denied"
        except Exception as e:
            return False, str(e)

    @classmethod
    def unblock(cls):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 cls._REG_PATH, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, cls._REG_KEY, 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            return True, None
        except FileNotFoundError:
            return True, None
        except PermissionError:
            return False, "permission_denied"
        except Exception as e:
            return False, str(e)

# ═══════════════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("fileguard.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger("FileGuard")

# ═══════════════════════════════════════════════════════════════════
#  ALERT STORE
# ═══════════════════════════════════════════════════════════════════

class AlertStore:
    def __init__(self):
        self._alerts = OrderedDict()
        self._lock   = threading.Lock()

    def add(self, a):
        with self._lock:
            self._alerts[a["id"]] = a
            while len(self._alerts) > MAX_ALERTS_MEMORY:
                self._alerts.popitem(last=False)

    def get(self, aid):
        with self._lock:
            return self._alerts.get(aid)

    def update_status(self, aid, status):
        with self._lock:
            if aid in self._alerts:
                self._alerts[aid]["status"] = status

    def pending(self):
        with self._lock:
            return [a for a in self._alerts.values()
                    if a["status"] == "pending"]

store = AlertStore()

# ═══════════════════════════════════════════════════════════════════
#  TELEGRAM HELPERS
# ═══════════════════════════════════════════════════════════════════

def _base():
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def tg_send(text, reply_markup=None, parse_mode="HTML"):
    timeout = 5 if _shutting_down else 10
    payload = {"chat_id": TELEGRAM_CHAT_ID,
               "text": text,
               "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(f"{_base()}/sendMessage",
                          json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except KeyboardInterrupt:
        return None
    except Exception as e:
        if not _shutting_down:
            log.error(f"Telegram send failed: {e}")
        return None

def tg_send_alert(alert):
    icon  = "📋" if alert["event"] == "copy" else "✂️"
    label = "COPIED" if alert["event"] == "copy" else "MOVED"
    aid   = alert["id"]
    text  = (
        f"🚨 <b>FILE TRANSFER DETECTED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{icon} <b>Event:</b> {label} to USB\n"
        f"📄 <b>File:</b> <code>{alert['file_name']}</code>\n"
        f"📦 <b>Size:</b> {alert['size']}\n"
        f"💾 <b>Drive:</b> {alert['drive']}\n"
        f"🕐 <b>Time:</b> {alert['time']}\n"
        f"🖥 <b>PC:</b> {DEVICE_NAME}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🆔 Alert ID: <code>{aid}</code>"
    )
    markup = {"inline_keyboard": [
        [
            {"text": "🗑 DELETE FILE",         "callback_data": f"delete_{aid}"},
            {"text": "✅ Allow",                "callback_data": f"allow_{aid}"},
        ],
        [
            {"text": "🗑🗑 DELETE ALL PENDING", "callback_data": "deleteall"},
            {"text": "🔒 LOCKDOWN",             "callback_data": "lockdown"},
        ]
    ]}
    tg_send(text, reply_markup=markup)

# ═══════════════════════════════════════════════════════════════════
#  DELETE HELPER
# ═══════════════════════════════════════════════════════════════════

def _try_delete(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True, "deleted"
        return True, "already_gone"
    except PermissionError:
        return False, "permission_denied"
    except Exception as e:
        return False, str(e)

# ═══════════════════════════════════════════════════════════════════
#  TELEGRAM POLLER
# ═══════════════════════════════════════════════════════════════════

class TelegramPoller:
    def __init__(self):
        self._offset = 0

    def start(self):
        threading.Thread(
            target=self._run, daemon=True, name="TgPoller").start()

    def _run(self):
        log.info("Telegram poller started")
        while not _shutting_down:
            try:
                self._poll()
            except KeyboardInterrupt:
                break
            except Exception as e:
                if not _shutting_down:
                    log.error(f"Polling error: {e}")
                time.sleep(3)

    def _poll(self):
        r = requests.get(
            f"{_base()}/getUpdates",
            params={"offset": self._offset, "timeout": 10},
            timeout=15)
        r.raise_for_status()
        for upd in r.json().get("result", []):
            self._offset = upd["update_id"] + 1
            try:
                self._handle(upd)
            except Exception as e:
                log.error(f"Handle error: {e}")

    def _handle(self, upd):
        if "callback_query" in upd:
            cq   = upd["callback_query"]
            data = cq.get("data", "")
            requests.post(f"{_base()}/answerCallbackQuery",
                          json={"callback_query_id": cq["id"]},
                          timeout=5)
            if   data == "deleteall":        self._deleteall()
            elif data == "lockdown":         self._lockdown()
            elif data == "unlock":           self._unlock()
            elif data.startswith("delete_"): self._delete(data[7:])
            elif data.startswith("allow_"):  self._allow(data[6:])
            return

        msg  = upd.get("message", {})
        text = msg.get("text", "").strip()
        if str(msg.get("chat", {}).get("id")) != str(TELEGRAM_CHAT_ID):
            return

        if   text == "/status":           self._status()
        elif text == "/list":             self._list()
        elif text == "/help":             self._help()
        elif text == "/deleteall":        self._deleteall()
        elif text == "/lockdown":         self._lockdown()
        elif text == "/unlock":           self._unlock()
        elif text.startswith("/delete_"): self._delete(text[8:])
        elif text.startswith("/allow_"):  self._allow(text[7:])

    # ── Commands ───────────────────────────────────────────────────

    def _status(self):
        mode   = "🔒 LOCKDOWN" if is_lockdown() else "🟢 Normal"
        markup = (
            {"inline_keyboard": [[
                {"text": "🔓 Unlock Now", "callback_data": "unlock"}]]}
            if is_lockdown() else
            {"inline_keyboard": [[
                {"text": "🔒 Enable Lockdown", "callback_data": "lockdown"},
                {"text": "🔓 Unlock",          "callback_data": "unlock"}]]}
        )
        tg_send(
            f"✅ <b>FileGuard is RUNNING</b>\n"
            f"🖥 Device: {DEVICE_NAME}\n"
            f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
            f"⚠️ Pending alerts: {len(store.pending())}\n"
            f"🛡 Mode: {mode}",
            reply_markup=markup)

    def _list(self):
        pending = store.pending()
        if not pending:
            tg_send("✅ No pending alerts. All clear.")
            return
        lines = [f"⚠️ <b>{len(pending)} pending alert(s):</b>\n"]
        for a in pending:
            lines.append(
                f"🆔 <code>{a['id']}</code> — {a['file_name']} ({a['size']})\n"
                f"/delete_{a['id']}  |  /allow_{a['id']}\n")
        tg_send("\n".join(lines),
                reply_markup={"inline_keyboard": [[
                    {"text": f"🗑🗑 DELETE ALL {len(pending)} FILES",
                     "callback_data": "deleteall"}]]})

    def _delete(self, aid):
        a = store.get(aid)
        if not a:
            tg_send(f"❌ Alert <code>{aid}</code> not found."); return
        if a["status"] != "pending":
            tg_send(f"ℹ️ Already {a['status']}."); return
        ok, reason = _try_delete(a["file_path"])
        if ok:
            store.update_status(aid, "deleted")
            if reason == "already_gone":
                tg_send(f"⚠️ File was already gone:\n<code>{a['file_path']}</code>")
            else:
                tg_send(f"🗑 <b>FILE DELETED</b>\n"
                        f"📄 <code>{a['file_name']}</code>\n✔️ Removed from USB.")
                log.warning(f"DELETED: {a['file_path']}")
        elif reason == "permission_denied":
            tg_send("❌ Permission denied. Run FileGuard as Administrator.")
        else:
            tg_send(f"❌ Delete failed: {reason}")

    def _deleteall(self):
        pending = store.pending()
        if not pending:
            tg_send("✅ No pending files to delete. All clear."); return
        deleted, failed, gone = [], [], []
        for a in pending:
            ok, reason = _try_delete(a["file_path"])
            if ok:
                store.update_status(a["id"], "deleted")
                if reason == "already_gone":
                    gone.append(a["file_name"])
                else:
                    deleted.append(a["file_name"])
                    log.warning(f"DELETED (bulk): {a['file_path']}")
            else:
                failed.append(f"{a['file_name']} ({reason})")
        parts = ["🗑🗑 <b>DELETE ALL — DONE</b>",
                 "━━━━━━━━━━━━━━━━━━━━━",
                 f"✅ Deleted: <b>{len(deleted)}</b> file(s)"]
        for n in deleted: parts.append(f"  🗑 <code>{n}</code>")
        if gone:  parts.append(f"\n⚠️ Already gone: {len(gone)} file(s)")
        if failed:
            parts.append(f"\n❌ Failed: {len(failed)} file(s)")
            for i in failed: parts.append(f"  ⛔ <code>{i}</code>")
            parts.append("\n💡 Run as Administrator to fix permission errors.")
        tg_send("\n".join(parts))

    def _lockdown(self):
        set_lockdown(True)
        ok, err = DriveBlocker.block()
        if ok:
            tg_send(
                "🔒 <b>LOCKDOWN ACTIVATED</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "🛑 USB drives are write-protected at OS level.\n"
                "Drag, copy, move — all blocked before data is written.\n\n"
                "Send /unlock to allow transfers again.",
                reply_markup={"inline_keyboard": [[
                    {"text": "🔓 Unlock — allow transfers",
                     "callback_data": "unlock"}]]})
        else:
            tg_send(
                f"⚠️ <b>LOCKDOWN — Partial Mode</b>\n"
                f"OS-level block failed: {err}\n"
                "Run as Administrator for full blocking.\n"
                "Fallback active: files deleted immediately after copy.",
                reply_markup={"inline_keyboard": [[
                    {"text": "🔓 Unlock", "callback_data": "unlock"}]]})
        log.warning(f"LOCKDOWN ON (OS: {'OK' if ok else 'FAIL — ' + str(err)})")

    def _unlock(self):
        if not is_lockdown():
            tg_send("ℹ️ FileGuard is already in normal alert mode."); return
        set_lockdown(False)
        ok, err = DriveBlocker.unblock()
        if ok:
            tg_send(
                "🔓 <b>LOCKDOWN DEACTIVATED</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━\n"
                "✅ USB drives are now writable.\n"
                "You will receive an alert for every file transferred.",
                reply_markup={"inline_keyboard": [[
                    {"text": "🔒 Re-enable Lockdown",
                     "callback_data": "lockdown"}]]})
        else:
            tg_send(f"⚠️ Unlock partial — could not restore write access: {err}")
        log.info(f"LOCKDOWN OFF (OS: {'OK' if ok else 'FAIL — ' + str(err)})")

    def _allow(self, aid):
        a = store.get(aid)
        if not a:
            tg_send(f"❌ Alert <code>{aid}</code> not found."); return
        store.update_status(aid, "allowed")
        tg_send(f"✅ <b>Allowed</b>\n📄 <code>{a['file_name']}</code> marked safe.")

    def _help(self):
        tg_send(
            "🛡 <b>FileGuard v2.4</b>\n"
            "👤 <b>Bhavya Jain</b> | <b>Techvyana2.0</b>\n\n"
            "📋 <b>Basic Commands</b>\n"
            "/status — Running status + current mode\n"
            "/list — Show pending alerts\n"
            "/delete_ID — Delete file by ID\n"
            "/allow_ID — Mark transfer as safe\n\n"
            "⚡ <b>Power Commands</b>\n"
            "/deleteall — Delete ALL pending files at once\n"
            "/lockdown — Block all USB writes at OS level\n"
            "/unlock — Return to normal alert mode\n\n"
            "Tap the buttons on any alert message for quick action.")

# ═══════════════════════════════════════════════════════════════════
#  FILE EVENT HANDLER
# ═══════════════════════════════════════════════════════════════════

class USBFileHandler(FileSystemEventHandler):
    def __init__(self, drive):
        self.drive = drive
        self._cache = {}

    def _watch_ok(self, path):
        return WATCH_ALL_FILES or \
               Path(path).suffix.lower() in PROTECTED_EXTENSIONS

    def _cooldown_ok(self, path):
        now = time.time()
        if now - self._cache.get(path, 0) < ALERT_COOLDOWN:
            return False
        self._cache[path] = now
        return True

    @staticmethod
    def _human(b):
        for u in ["B","KB","MB","GB"]:
            if b < 1024: return f"{b:.1f} {u}"
            b /= 1024
        return f"{b:.1f} TB"

    def _make_alert(self, etype, path):
        try:   sz = self._human(os.path.getsize(path))
        except: sz = "unknown"
        aid = hashlib.md5(f"{path}{time.time()}".encode()).hexdigest()[:8]
        return {"id": aid, "event": etype,
                "file_name": os.path.basename(path),
                "file_path": path, "drive": self.drive,
                "size": sz,
                "time": datetime.now().strftime("%H:%M:%S"),
                "status": "pending"}

    def _handle(self, etype, path):
        if _shutting_down: return
        if not self._watch_ok(path):   return
        if not self._cooldown_ok(path): return
        name = os.path.basename(path)
        if name.startswith(("~$", ".")) or name.endswith(".tmp"): return

        if is_lockdown():
            ok, reason = _try_delete(path)
            if ok:
                log.warning(f"[LOCKDOWN BYPASS] Deleted: {path}")
                tg_send(f"⚠️ <b>LOCKDOWN — File Bypassed & Deleted</b>\n"
                        f"📄 <code>{name}</code>\n🗑 Deleted immediately.")
            else:
                log.error(f"[LOCKDOWN] Could not delete {path}: {reason}")
                tg_send(f"🚨 <b>LOCKDOWN BREACH — Delete Failed</b>\n"
                        f"📄 <code>{name}</code>\n❌ Reason: {reason}\n"
                        "💡 Run FileGuard as Administrator.")
            return

        alert = self._make_alert(etype, path)
        store.add(alert)
        log.info(f"ALERT [{etype}]: {path}")
        tg_send_alert(alert)

    def on_created(self, e):
        if not e.is_directory: self._handle("copy", e.src_path)

    def on_moved(self, e):
        if not e.is_directory: self._handle("move", e.dest_path)

# ═══════════════════════════════════════════════════════════════════
#  USB MONITOR
# ═══════════════════════════════════════════════════════════════════

class USBMonitor:
    def __init__(self, on_connect, on_disconnect):
        self.on_connect    = on_connect
        self.on_disconnect = on_disconnect
        self.known         = set(self._removable())

    def _removable(self):
        out = []
        for p in psutil.disk_partitions():
            try:
                if win32file.GetDriveType(p.mountpoint) == win32con.DRIVE_REMOVABLE:
                    out.append(p.mountpoint)
            except Exception:
                pass
        return out

    def start(self):
        threading.Thread(
            target=self._run, daemon=True, name="USBMonitor").start()

    def _run(self):
        log.info(f"USB monitor running. Connected: {self.known or 'none'}")
        while not _shutting_down:
            try:
                cur = set(self._removable())
                for d in cur - self.known:
                    log.info(f"USB connected: {d}")
                    self.on_connect(d)
                for d in self.known - cur:
                    log.info(f"USB disconnected: {d}")
                    self.on_disconnect(d)
                self.known = cur
            except Exception as e:
                if not _shutting_down:
                    log.error(f"USB monitor error: {e}")
            time.sleep(2)

# ═══════════════════════════════════════════════════════════════════
#  MAIN AGENT
# ═══════════════════════════════════════════════════════════════════

class FileGuardAgent:
    def __init__(self):
        self.observers   = {}
        self._stop_event = threading.Event()

    def _validate(self):
        r = requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe",
            timeout=10)
        if not r.ok or not r.json().get("ok"):
            log.error(f"Bot token invalid: {r.text}")
            sys.exit(1)
        log.info(f"Bot verified: @{r.json()['result']['username']}")

    def start(self):
        self._validate()
        signal.signal(signal.SIGINT,  self._sig)
        signal.signal(signal.SIGTERM, self._sig)

        tg_send(
            f"🛡 <b>FileGuard v2.4 Started</b>\n"
            f"👤 <b>Bhavya Jain</b> | <b>Techvyana2.0</b>\n"
            f"🖥 Device: {DEVICE_NAME}\n"
            f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "Monitoring USB drives for file transfers.\n"
            "Send /help for commands.",
            reply_markup={"inline_keyboard": [
                [
                    {"text": "📋 Status",      "callback_data": "status_noop"},
                    {"text": "📜 List Alerts", "callback_data": "list_noop"},
                ],
                [
                    {"text": "🗑🗑 Delete All", "callback_data": "deleteall"},
                    {"text": "🔒 Lockdown",    "callback_data": "lockdown"},
                ]
            ]}
        )

        TelegramPoller().start()

        usb = USBMonitor(self._watch, self._unwatch)
        for d in usb.known:
            self._watch(d)
        usb.start()

        log.info("FileGuard is running. Press Ctrl+C to stop.")
        self._stop_event.wait()
        self._shutdown()

    def _sig(self, signum, frame):
        global _shutting_down
        _shutting_down = True
        log.info("Shutdown signal — stopping cleanly…")
        self._stop_event.set()

    def _watch(self, drive):
        if drive in self.observers: return
        log.info(f"Starting watcher on {drive}")
        try:
            h   = USBFileHandler(drive)
            obs = PollingObserver(timeout=2)
            obs.schedule(h, drive, recursive=True)
            obs.start()
            self.observers[drive] = obs
            mode = ("🔒 <b>LOCKDOWN</b> — files deleted on arrival"
                    if is_lockdown() else "✅ Normal — alerts sent")
            tg_send(f"🔌 <b>USB Connected:</b> {drive}\n🛡 Mode: {mode}")
        except Exception as e:
            log.error(f"Could not watch {drive}: {e}")
            tg_send(f"❌ Failed to monitor {drive}: {e}")

    def _unwatch(self, drive):
        if drive in self.observers:
            try:
                self.observers[drive].stop()
                self.observers[drive].join(timeout=3)
            except Exception:
                pass
            del self.observers[drive]
            if not _shutting_down:
                tg_send(f"🔌 USB removed: {drive}")

    def _shutdown(self):
        log.info("Shutting down watchers…")
        for obs in self.observers.values():
            try:
                obs.stop()
                obs.join(timeout=3)
            except Exception:
                pass
        try:
            tg_send(
                f"🛑 <b>FileGuard stopped</b> on {DEVICE_NAME}\n"
                "👤 Bhavya Jain | Techvyana2.0")
        except Exception:
            pass
        log.info("FileGuard stopped cleanly. Goodbye.")

# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Show Setup UI (skipped if valid config already exists)
    token, chat_id, device_name = get_config()

    # 2. Inject into module-level globals
    TELEGRAM_TOKEN   = token
    TELEGRAM_CHAT_ID = chat_id
    DEVICE_NAME      = device_name

    # 3. Launch the agent
    FileGuardAgent().start()
