import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BOARD)

bouton = 16
GPIO.setup(bouton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

etatPrecedent = 0

while True:
    etat = GPIO.input(bouton)

    if etat != etatPrecedent:
        if etat:
            print("Appuyé")
        else:
            print("Relâché")

        etatPrecedent = etat

    t.sleep(0.05)