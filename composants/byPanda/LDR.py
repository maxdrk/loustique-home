import RPi.GPIO as GPIO

LDR_PIN = 20


GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)

def lire_etat():
    if GPIO.input(LDR_PIN) == GPIO.HIGH:
        return "Nuit"
    return "Jour"