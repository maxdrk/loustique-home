import time
from ALARM_V1 import *
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
            ALARM_V1.boucle_principale()
            porte.mettreAJour()
            time.sleep(0.05)

    except KeyboardInterrupt:
        porte.cleanup()
        alarme.cleanup()
        print("\nArrêt manuel du programme.")

    finally:
        # On remet les sorties dans un état propre avant de quitter
        alarme.cleanup()
        porte.cleanup()
