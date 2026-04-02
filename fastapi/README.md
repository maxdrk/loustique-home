🏠 Projet IoT : API de Contrôle Domotique (Raspberry Pi 2)

Ce dépôt contient le code du Serveur API déployé sur le deuxième Raspberry Pi. Son rôle est de piloter les composants physiques (LED, Thermostat, Afficheurs) en répondant aux requêtes envoyées par le Raspberry Pi 1.
🏗️ Architecture du Système

Le projet repose sur une architecture distribuée :

    Raspberry Pi 1 (Client) : Envoie les requêtes HTTP/HTTPS.

    Raspberry Pi 2 (Serveur - Ce repo) : Reçoit les ordres, exécute la logique métier via les GPIO et renvoie l'état du système.

🛠️ Installation Rapide

Un script d'automatisation est fourni pour configurer l'environnement, les bases de données et les dépendances.
Bash

# 1. Rendre le script exécutable
chmod +x main.sh

# 2. Lancer l'installation (nécessite les droits sudo)
sudo ./main.sh

Ce que fait le script main.sh :

    Mise à jour du système (apt update & upgrade).

    Installation optionnelle de MariaDB et phpMyAdmin.

    Configuration d'un environnement virtuel Python (venv).

    Installation des dépendances via requirement.txt.

🚀 Lancement du Serveur

Pour démarrer l'API, utilisez le script de lancement qui vérifie les prérequis (Python, SSL, Avahi) avant de lancer Uvicorn :
Bash

chmod +x run_api.sh
sudo ./run_api.sh

Note : Le serveur utilise HTTPS. Les certificats doivent être présents dans ../web_secu/ssl/.
📡 Points d'entrée de l'API (Endpoints)

L'API est documentée automatiquement (Swagger) via FastAPI à l'adresse : https://<IP_DU_PI>:8000/docs
Méthode	Route	Description
GET	/up_led	Allume les lumières et active le mode manuel.
GET	/down_led	Éteint les lumières et active le mode manuel.
GET	/temperature	Lit le capteur DHT11 et affiche la valeur sur le 7 segments.
📂 Structure du Code Python (main.py)

Le serveur utilise une approche modulaire pour gérer les composants :

    SystemeLumieres : Gestion des LEDs.

    SystemeThermostat : Lecture des données capteurs.

    EtatSysteme : Gestion visuelle des erreurs/succès (LED d'état).

    afficher_temperature : Pilotage de l'afficheur TM1637.

📋 Dépendances Principales

    FastAPI & Uvicorn : Framework web et serveur ASGI.

    RPi.GPIO : Contrôle des broches du Raspberry Pi.

    Adafruit_DHT : Lecture des capteurs d'humidité et température.

    python-tm1637 : Driver pour l'afficheur 7 segments.

⚠️ Notes de Sécurité

    Le serveur est configuré avec CORS autorisant toutes les origines ("*") pour faciliter le développement.

    La communication est sécurisée par SSL (TLS).

    Le service Avahi est utilisé pour la résolution de noms sur le réseau local.

API Développée par les loustiques