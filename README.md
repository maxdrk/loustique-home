# 🏠 Loustiques Home

> Projet domotique conçu par le groupe **Les Loustiques** de l'EPHEC.

---

## Contexte

Les Loustiques est un groupe d'étudiants de l'EPHEC qui conçoit une maison domotique pilotée par un **Raspberry Pi 2**. L'objectif est de contrôler des équipements physiques (LED, capteurs, etc.) via une interface web sécurisée, accessible depuis le réseau local.

L'application repose sur un serveur **Flask** (Python) qui expose une API et sert les pages HTML. L'authentification est gérée via une base de données **MySQL**, et les actions physiques sont déclenchées via la bibliothèque **gpiozero** qui communique avec les GPIOs du Raspberry Pi.

---

## Architecture du projet

```
loustiques-home/
├── flask/
│   ├── main.py            # Point d'entrée Flask — routes et API
│   ├── auth.py            # Authentification et gestion des utilisateurs
│   ├── add_user.py        # Ajout d'utilisateur (appelé par l'admin)
│   ├── led.py             # Contrôle de la LED via GPIO
│   ├── log.py             # Configuration du système de logs
│   └── templates/
│       ├── index.html     # Page de connexion
│       ├── dashboard.html # Tableau de bord principal
│       ├── admin.html     # Panneau d'administration
│       └── log.html       # Visualisation des logs en temps réel
├── web_secu/
│   ├── ssl.sh             # Génération du certificat SSL auto-signé
│   ├── avahi.sh           # Installation et démarrage du service mDNS
│   └── ssl/
│       ├── cert.pem       # Certificat SSL (généré automatiquement)
│       └── key.pem        # Clé privée SSL (générée automatiquement)
├── run_flask.sh           # Script de démarrage du serveur
├── requirement.txt        # Dépendances Python
└── .env                   # Variables d'environnement (non versionné)
```

---

## Description des fichiers

### `run_flask.sh`

Script bash de démarrage. Il vérifie la présence de Python 3 et de Flask, génère le certificat SSL si absent, démarre Avahi pour le DNS local, crée le fichier de log `/var/log/loustique.log` avec les bonnes permissions, puis lance le serveur Flask.

À exécuter avec `sudo` pour pouvoir créer le fichier de log et installer les services :

```bash
sudo bash run_flask.sh
```

---

### `web_secu/ssl.sh`

Génère un certificat SSL auto-signé (`cert.pem` + `key.pem`) dans `web_secu/ssl/`. Le certificat est valable 365 jours et est émis pour `loustiques.local`. Si le certificat existe déjà, le script ne le régénère pas.

```
C=BE / ST=Brabant Wallon / L=Louvain-La-Neuve / O=Les Loustiques / OU=EPHEC / CN=loustiques.local
```

---

### `web_secu/avahi.sh`

Installe et démarre **Avahi** (implémentation mDNS) sur le Raspberry Pi. Une fois actif, le Pi est automatiquement accessible via son hostname suivi de `.local` sur tout le réseau local, sans rien modifier sur les machines clientes.

Pour changer le hostname du Pi :

```bash
sudo hostnamectl set-hostname loustiques
sudo reboot
```

Le Pi sera ensuite accessible via `https://loustiques.local:5000`.

---

### `log.py`

Configure le système de logging de l'application. Les logs sont écrits dans `/var/log/loustique.log` au format :

```
2026-03-24 22:07:44,532 - loustique - INFO - Connexion réussie pour maxime
```

Le logger `werkzeug` (serveur Flask interne) est également redirigé vers ce fichier pour centraliser tous les événements. La propagation vers la console est désactivée pour éviter les doublons et les codes couleur ANSI.

---

### `auth.py`

Gère l'authentification des utilisateurs et la récupération des comptes.

- `init()` — ouvre une connexion MySQL à partir des variables d'environnement `.env`
- `login(username, password)` — vérifie les identifiants en comparant le mot de passe avec le hash bcrypt stocké en base
- `get_users()` — retourne la liste de tous les utilisateurs (username, rôle, date de création)

---

### `add_user.py`

Permet d'ajouter un nouvel utilisateur en base de données. Cette fonction est appelée par la route `/admin/add_user` de Flask. Le mot de passe est hashé avec **bcrypt** avant d'être stocké. Le rôle (`admin` ou `user`) est passé directement en paramètre.

---

### `led.py`

Contient la fonction `led(utilisateur)` qui simule (ou déclenche réellement sur le Pi) l'allumage d'une LED. Le code GPIO est commenté pour permettre les tests hors Raspberry Pi. Chaque déclenchement est logué avec le nom de l'utilisateur qui en est à l'origine.

---

### `main.py`

Point d'entrée de l'application Flask. Définit toutes les routes :

| Route | Méthode | Description |
|---|---|---|
| `/` | GET | Page de connexion |
| `/login` | POST | Authentifie l'utilisateur |
| `/dashboard` | GET | Tableau de bord |
| `/led` | POST | Déclenche la LED |
| `/admin` | GET | Panneau d'administration |
| `/admin/add_user` | POST | Crée un nouvel utilisateur |
| `/admin/get_users` | GET | Liste tous les utilisateurs |
| `/admin/logs` | GET | Page de visualisation des logs |
| `/admin/logs/data` | GET | Retourne les logs en JSON |

L'utilisateur connecté est stocké dans la variable globale `current_user` pour être transmis aux fonctions comme `led()`.

---

### `index.html`

Page de connexion. Envoie les identifiants en JSON vers `/login` et redirige vers `/dashboard` en cas de succès.

---

### `dashboard.html`

Tableau de bord principal. Affiche l'heure locale, le statut du système, et propose des actions rapides : allumer la LED, accéder à l'administration, etc.

---

### `admin.html`

Panneau d'administration. Permet de créer de nouveaux utilisateurs (avec choix du rôle et indicateur de force du mot de passe) et de lister les comptes existants avec la possibilité de les supprimer.

---

### `log.html`

Interface de visualisation des logs en temps réel. Se rafraîchit automatiquement toutes les 5 secondes via un fetch vers `/admin/logs/data`. Propose un filtrage par niveau (INFO, WARNING, ERROR, DEBUG) et une barre de recherche.

---

## Installation

### Prérequis

- Raspberry Pi 2 sous Linux (Raspbian recommandé)
- Python 3.11+
- MySQL / MariaDB
- Un environnement virtuel Python (`venv`)

> **Note :** Le script `run_flask.sh` s'occupe automatiquement de vérifier et installer les dépendances nécessaires. Cette liste est fournie par souci de transparence et pour les installations manuelles.

### Étapes

```bash
# Cloner le dépôt
git clone git@github.com:maxdrk/loustique-home.git
cd loustique-home

# Créer et activer le venv
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirement.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos infos MySQL

# Lancer le serveur
sudo bash run_flask.sh
```

---

## Accès à l'interface

Une fois le serveur lancé, l'interface est accessible via :

```
https://<hostname>.local:5000
```

Le certificat étant auto-signé, le navigateur affichera un avertissement de sécurité. Il suffit d'accepter l'exception pour continuer.

---

## Variables d'environnement (`.env`)

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe
DB_NAME=loustique
DB_CHARSET=utf8mb4
```

---

## Structure de la base de données

```sql
CREATE TABLE Auth (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    Fonctions VARCHAR(20) NOT NULL,  -- 'admin' ou 'user'
    created_at DATETIME NOT NULL
);
```

---

## Dépendances (`requirement.txt`)

| Package | Rôle |
|---|---|
| `flask` | Serveur web |
| `pymysql` | Connexion MySQL |
| `bcrypt` | Hashage des mots de passe |
| `python-dotenv` | Chargement du fichier `.env` |
| `gpiozero` | Contrôle des GPIOs du Raspberry Pi |

---

## Groupe

Projet réalisé par **Les Loustiques** — étudiants à l'**EPHEC** (Louvain-La-Neuve).