import RPi.GPIO as GPIO
import time as t


servo_pin = 18
bouton_up = 27
bouton_down = 16
etat_porte = "Fermé"

def get_etat(etat):
    global etat_porte
    etat_porte = etat
    print(f"État mis à jour : {etat_porte}")

def test_boutons():
    global etat_porte

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(bouton_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(bouton_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)

    etatPrecedent_up = GPIO.input(bouton_up)
    etatPrecedent_down = GPIO.input(bouton_down)

    print("Thread Servo : Démarré et prêt.")

    try:
        while True:
            etat_up = GPIO.input(bouton_up)
            etat_down = GPIO.input(bouton_down)

            if etat_up != etatPrecedent_up:
                if etat_up == GPIO.LOW:
                    get_etat('Ouvert')
                    pwm.ChangeDutyCycle(2.5)
                    t.sleep(0.5)
                    pwm.ChangeDutyCycle(0)
                etatPrecedent_up = etat_up

            if etat_down != etatPrecedent_down:
                if etat_down == GPIO.LOW:
                    get_etat('Fermé')
                    pwm.ChangeDutyCycle(7.5)
                    t.sleep(0.5)
                    pwm.ChangeDutyCycle(0)
                etatPrecedent_down = etat_down

            t.sleep(0.05)
    except Exception as e:
        print(f"Erreur dans le thread servo : {e}")
    finally:
        pwm.stop()
       
#test_boutons()
