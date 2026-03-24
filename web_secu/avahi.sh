#!/bin/bash
cat << 'EOF'
=============================
  _______   ________  ___  ___  _______   ________     
|\  ___ \ |\   __  \|\  \|\  \|\  ___ \ |\   ____\    
\ \   __/|\ \  \|\  \ \  \\\  \ \   __/|\ \  \___|    
 \ \  \_|/_\ \   ____\ \   __  \ \  \_|/_\ \  \       
  \ \  \_|\ \ \  \___|\ \  \ \  \ \  \_|\ \ \  \____  
   \ \_______\ \__\    \ \__\ \__\ \_______\ \_______\
    \|_______|\|__|     \|__|\|__|\|_______|\|_______|
 =============================
EOF


if dpkg -l avahi-daemon 2>/dev/null | grep -q '^ii'; then
    echo "Avahi est déjà installé et actif."
else
    apt install -y avahi-daemon
    systemctl enable avahi-daemon
    systemctl start avahi-daemon
    echo "Avahi démarré — accessible via loustiques.local"
fi