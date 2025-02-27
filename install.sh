#!/bin/bash

# System aktualisieren
sudo apt update && sudo apt upgrade -y

# Python3 und pip installieren
sudo apt install python3 -y
sudo apt install python3-pip -y

# Benötigte Python-Pakete installieren
sudo pip3 install requests psutil

# Skript herunterladen (wenn es auf GitHub gehostet wird)
git clone https://github.com/username/repository.git /root/change_password_project
cd /root/change_password_project

# bashrc für automatische Ausführung anpassen
echo 'python3 /root/change_password_project/change_password.py' >> ~/.bashrc

# Run-Skript erstellen
echo -e '#!/bin/bash\npython3 /root/change_password_project/change_password.py' > /root/run_change_password.sh
chmod +x /root/run_change_password.sh

# Optional: Crontab für halb-stündliche Ausführung setzen
(crontab -l 2>/dev/null; echo "*/30 * * * * /root/run_change_password.sh") | crontab -
