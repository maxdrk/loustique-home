#!/bin/bash

cat << 'EOF'
=======================
Vérification de mariaDB
===========================
EOF

echo "Vérification / Installation de mariadb..."
if ! apt install mariadb-server -y; then
    echo "Erreur lors de l'installation de mariadb-server"
    exit 1
fi
MARIADB_VERSION=$(mariadb --version 2>&1)
echo "$MARIADB_VERSION installé"
sleep 1

echo "Vérification / Installation de phpMyAdmin..."
if ! apt install phpmyadmin -y; then
    echo "Erreur lors de l'installation de phpMyAdmin"
    exit 1
fi
PHP_VERSION=$(php --version 2>&1 | head -n 1)
echo "$PHP_VERSION installé"
sleep 1