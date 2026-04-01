import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
servo = 12
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo, 50)
pwm.start(0)
bouton_up = 13
bouton_down = 36
GPIO.setup(bouton_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bouton_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_boutons():
    etatPrecedent_up = GPIO.input(bouton_up)
    etatPrecedent_down = GPIO.input(bouton_down)

    print("Test lancé ! Appuie sur UP (23) pour monter, DOWN (24) pour descendre.")

    while True:
        etat_up = GPIO.input(bouton_up)
        etat_down = GPIO.input(bouton_down)
        if etat_up != etatPrecedent_up:
            if etat_up == 0:
                print("Bouton UP Appuyé ⬆️")
                print("Volet ouvert")
                pwm.ChangeDutyCycle(2)
            etatPrecedent_up = etat_up
        if etat_down != etatPrecedent_down:
            if etat_down == 0:
                print("Bouton DOWN Appuyé ⬇️")
                print("Volet fermé")
                pwm.ChangeDutyCycle(7)
            etatPrecedent_down = etat_down
        t.sleep(0.05)

if name == "main":
    try:
        test_boutons()
    except KeyboardInterrupt:
        print("\nFin du test")