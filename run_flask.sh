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
cat << 'EOF'
===============================
Vérification de la présence de python
=================================
EOF

VERSION_PYTHON=$(python3 --version 2>&1)

if [ $? -eq 0 ]; then
    echo "Python est installé"
    echo "Voici la version : $VERSION_PYTHON"
else
    apt install -y python3
fi

cat << 'EOF'
===================================================
Vérification de la présence de la bibliothèque FLASK
====================================================
EOF

if venv/bin/python -m pip list | grep -qi 'flask'; then
    echo "Flask existe bien"
else
    echo "Flask n'est pas installé..."
    echo "Lancement de l'installation..."
    sleep 1
    venv/bin/python -m pip install flask
fi

cat << 'EOF'
================================
Lancement du serveur FLASK
================================
EOF

sleep 1
venv/bin/python ./flask/main.py
