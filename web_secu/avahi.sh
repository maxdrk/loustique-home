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


if systemctl is-active --quiet avahi-daemon; then
    echo "Avahi est déjà actif  accessible via $(hostname).local"
else
    if ! dpkg -l avahi-daemon 2>/dev/null | grep -q '^ii'; then
        echo "Installation de Avahi..."
        apt install -y avahi-daemon
    fi
    systemctl enable avahi-daemon
    systemctl start avahi-daemon
    echo "Avahi démarré  accessible via $(hostname).local"
fi