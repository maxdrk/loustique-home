#!/bin/bash

if [ -d "web_secu/ssl" ]; then
    echo "Le dossier ssl existe déjà"
    chown ${SUDO_USER}:${SUDO_USER} web_secu/ssl/
else
    mkdir -p web_secu/ssl
    chown ${SUDO_USER}:${SUDO_USER} web_secu/ssl/
    echo "Dossier ssl créé"
fi

if [ -f "web_secu/ssl/cert.pem" ] && [ -f "web_secu/ssl/key.pem" ]; then
    echo "Certificat SSL déjà existant"
else
    openssl req -x509 -newkey rsa:4096 -keyout web_secu/ssl/key.pem -out web_secu/ssl/cert.pem -days 365 -nodes \
        -subj "/C=BE/ST=Brabant Wallon/L=Louvain-La-Neuve/O=Les Loustiques/OU=EPHEC/CN=loustiques.local"
    echo "Certificat généré avec succès"
fi