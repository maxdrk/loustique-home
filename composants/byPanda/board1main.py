import time
import threading
import alarme
from porterfid import SystemePorteRFID
import RPi.GPIO as GPIO

porte = SystemePorteRFID()

def call_board1():
    # 1. On lance l'alarme dans son propre thread pour qu'elle ne bloque pas le reste
    thread_alarme = threading.Thread(target=alarme.boucle_principale, daemon=True)
    thread_alarme.start()

    print("[BOARD 1] Système d'alarme lancé en arrière-plan.")

    try:
        # 2. La boucle principale ne gère plus que le RFID
        while True:
            porte.mettreAJour()
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\nArrêt manuel du programme.")
    finally:
        # On utilise GPIO.cleanup() directement car alarme.cleanup n'existe pas
        porte.cleanup()
        GPIO.cleanup()