#!/bin/bash

cat << 'EOF'

 _______   ________  ___  ___  _______   ________     
|\  ___ \ |\   __  \|\  \|\  \|\  ___ \ |\   ____\    
\ \   __/|\ \  \|\  \ \  \\\  \ \   __/|\ \  \___|    
 \ \  \_|/_\ \   ____\ \   __  \ \  \_|/_\ \  \       
  \ \  \_|\ \ \  \___|\ \  \ \  \ \  \_|\ \ \  \____  
   \ \_______\ \__\    \ \__\ \__\ \_______\ \_______\
    \|_______|\|__|     \|__|\|__|\|_______|\|_______|
                                                      
                                                      
                                                      
EOF



# ==============================================
# Script de configuration automatique Raspberry Pi - Projet IoT
# ==============================================

set -euo pipefail

SEPARATOR="=============================================="

print_step() {
    echo ""
    echo "$SEPARATOR"
    echo "  $1"
    echo "$SEPARATOR"
}

# Vérification des droits sudo
if [ "$EUID" -ne 0 ]; then
    echo "  Ce script doit être exécuté avec sudo"
    echo "    Utilisation : sudo ./main.sh"
    exit 1
fi

print_step " Lancement du programme de configuration IoT"
print_step " Lancement du programme de configuration IoT"
sleep 1

# ----------------------------
# 1. Mise à jour du système
# ----------------------------
print_step " Mise à jour du système (apt update & upgrade)"
print_step " Mise à jour du système (apt update & upgrade)"
if ! apt update && apt upgrade -y; then
    echo " Erreur lors de la mise à jour du système"
    exit 1
fi
echo "Système mis à jour"
sleep 1

# ----------------------------
# 2. Installation de Python
# ----------------------------
print_step "Vérification / Installation de Python3"
if ! apt install python3 python3-pip python3-venv -y; then
    echo "Erreur lors de l'installation de Python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo " $PYTHON_VERSION installé"
echo " $PYTHON_VERSION installé"
sleep 1

# ----------------------------
# 3. Recherche des venvs existants
# ----------------------------
print_step "Recherche des environnements virtuels (venv) existants..."

SEARCH_DIRS=("$(pwd)")
VENV_LIST=()

for dir in "${SEARCH_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        # Un venv valide contient bin/activate et bin/python
        while IFS= read -r -d '' activate_path; do
            venv_dir=$(dirname "$(dirname "$activate_path")")
            if [ -f "$venv_dir/bin/python" ]; then
                VENV_LIST+=("$venv_dir")
            fi
        done < <(find "$dir" -name "activate" -path "*/bin/activate" 2>/dev/null -print0)
    fi
done

echo ""
if [ ${#VENV_LIST[@]} -eq 0 ]; then
    echo "  Aucun environnement virtuel trouvé dans : $(pwd)"
else
    echo "${#VENV_LIST[@]} environnement(s) virtuel(s) trouvé(s) :"
    for i in "${!VENV_LIST[@]}"; do
        venv="${VENV_LIST[$i]}"
        python_ver=$("$venv/bin/python" --version 2>&1)
        echo ""
        echo "  [$((i+1))]  Chemin  : $venv"
        echo "        Python  : $python_ver"
        echo "       ▶  Activer : source $venv/bin/activate"
    done
    SELECTED_VENV="${VENV_LIST[0]}"
    echo "$SELECTED_VENV" > ./.venv_path
    echo ""
    echo "Venv sélectionné et enregistré : $SELECTED_VENV"
fi

# ----------------------------
# 4. Créer un nouveau venv ?
# ----------------------------
print_step " Créer un nouvel environnement virtuel ?"
echo "Voulez-vous créer un nouveau venv ? (o/n)"
read -r CREATE_VENV

if [[ "$CREATE_VENV" =~ ^[oO]$ ]]; then
	VENV_PATH="$SEARCH_DIRS/venv"
        if python3 -m venv $SEARCH_DIRS/venv; then
            echo ""
            echo "Venv créé avec succès !"
            echo "    Chemin  : $VENV_PATH"
            echo "   ▶  Activer : source $VENV_PATH/bin/activate"

            
            echo "$VENV_PATH" > ./.venv_path
            echo "Chemin enregistré dans .venv_path"

         
            "$VENV_PATH/bin/pip" install --upgrade pip

           
            if [ -f "./requirements.txt" ]; then
                echo "Installation des dépendances depuis requirements.txt..."
                "$VENV_PATH/bin/pip" install -r ./requirements.txt
                echo " Dépendances installées"
                echo " Dépendances installées"
            else
                echo " Aucun requirements.txt trouvé, installation des dépendances ignorée"
                echo " Aucun requirements.txt trouvé, installation des dépendances ignorée"
            fi
        else
            echo " Erreur lors de la création du venv à : $VENV_PATH"
            echo " Erreur lors de la création du venv à : $VENV_PATH"
            exit 1
        
    fi
else
    echo " Création ignorée"
    echo " Création ignorée"
fi

# ----------------------------
# Fin
# ----------------------------
print_step " Configuration terminée"
print_step " Configuration terminée"
echo ""
if [ -f "./.venv_path" ]; then
    echo "Venv configuré : $(cat ./.venv_path)"
    echo "    Pour l'activer manuellement : source $(cat ./.venv_path)/bin/activate"
else
    echo " Aucun venv enregistré — relancez le script et créez un venv"
fi
echo ""
