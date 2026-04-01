import time
from alarme import SystemeAlarme
from porterfid import SystemePorteRFID

# ------------------------------------------------------------
# board1main.py
# ------------------------------------------------------------
# Ce fichier lance uniquement la logique locale de la board 1.
# Il ne dépend pas du site web, de la base de données ni de Flask.
# Son rôle est simplement de faire tourner :
# - le système d'alarme
# - le système de porte RFID
# ------------------------------------------------------------

alarme = SystemeAlarme()
porte = SystemePorteRFID()


def call_board1():
    try:
        while True:
            # Mise à jour des deux modules locaux
            alarme.mettreAJour()
            porte.mettreAJour()
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nArrêt manuel du programme.")

    finally:
        # On remet les sorties dans un état propre avant de quitter
        alarme.cleanup()
        porte.cleanup()
