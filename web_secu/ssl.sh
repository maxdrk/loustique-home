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


EOF

mkdir ssl
chown ${SUDO_USER}:${SUDO_USER} ssl/

if [ -f "web_secu/ssl/cert.pem" ] && [ -f "web_secu/ssl/key.pem" ]; then
    echo "Certificat SSL déjà existant, on passe."
else
    mkdir -p web_secu/ssl
    openssl req -x509 -newkey rsa:4096 -keyout web_secu/ssl/key.pem -out web_secu/ssl/cert.pem -days 365 -nodes \
        -subj "/C=BE/ST=Brabant Wallon/L=Louvain-La-Neuve/O=Les Loustiques/OU=EPHEC/CN=loustiques.local"
    echo "Certificat généré avec succès !"
fi