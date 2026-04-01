import RPi.GPIO as GPIO
import time

# Configuration
LDR_PIN = 20# Broche GPIO connectée au circuit LDR
SEUIL = 500  # Valeur de seuil à ajuster (0-1024)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)


def lire_ldr():
    # Simulation de lecture analogique (nécessite MCP3008 ou circuit RC)
    # Pour cet exemple, on simplifie par une lecture numérique
    return GPIO.input(LDR_PIN) 

try:
    while True:
        luminosite = lire_ldr()
        if luminosite < SEUIL:
            print("Nuit : Allumage lumière")
        else:
            print("Jour : Extinction lumière")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
