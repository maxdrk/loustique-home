import time
import threading
import alarme
from porterfid import SystemePorteRFID
import RPi.GPIO as GPIO

porte = SystemePorteRFID()

def call_board1():
    thread_alarme = threading.Thread(target=alarme.boucle_principale, daemon=True)
    thread_alarme.start()

    print("[BOARD 1] Système d'alarme lancé en arrière-plan.")

    try:
        while True:
            porte.mettreAJour()
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\nArrêt manuel du programme.")
    finally:
        porte.cleanup()
        GPIO.cleanup()