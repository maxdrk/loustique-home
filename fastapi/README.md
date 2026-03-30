# Serveur FastAPI

## Description

Ce serveur **FastAPI** est destiné à être déployé sur le **deuxième Raspberry Pi** de l’architecture.

Son rôle principal est de **gérer et traiter toutes les requêtes envoyées par le Raspberry Pi 1**, afin de centraliser la logique de traitement et d’assurer une communication fluide entre les deux الأجهزة.

---

## Architecture

* **Raspberry Pi 1**

  * Envoie les requêtes (HTTP/API)
  * Sert de client / déclencheur

* **Raspberry Pi 2 (ce serveur)**

  * Héberge le serveur FastAPI
  * Reçoit, traite et répond aux requêtes
  * Exécute la logique métier

---

## Installation

Pour garantir une installation propre et optimale, il est recommandé d’utiliser le script fourni.

### 1. Cloner le projet

```bash
git clone <repo_url>
cd <repo>
```

### 2. Lancer l’installation automatique

Le script `main.sh` permet de :

* créer un environnement virtuel Python (`venv`)
* installer toutes les dépendances nécessaires
* configurer l’environnement correctement

```bash
chmod +x main.sh
./main.sh
```

---

## Environnement virtuel

Le projet utilise **Python venv** pour isoler les dépendances.

Si besoin, activation manuelle :

```bash
source venv/bin/activate
```

---

## Dépendances

Les dépendances sont listées dans le fichier :

```
requirements.txt
```

Elles sont automatiquement installées via le script `main.sh`.

---

## Lancement du serveur

Une fois l’installation terminée, le serveur peut être lancé avec :

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Objectif

Ce serveur a pour objectif de :

* centraliser le traitement des requêtes
* améliorer les performances globales du système
* permettre une architecture distribuée entre plusieurs Raspberry Pi

---

## Notes

* Assurez-vous que les deux Raspberry Pi sont sur le même réseau.
* Vérifiez les ports et adresses IP pour permettre la communication entre les deux machines.
* Adapter la configuration si nécessaire selon votre environnement.

---
