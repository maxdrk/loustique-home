import RPi.GPIO as GPIO
import time as t
from septsegments import afficher_temperature
from DHT11 import lire_temperature

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

bouton_up = 23
bouton_down = 24 
GPIO.setup(bouton_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bouton_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_boutons():
    temperature_DHT = lire_temperature()
    temperature_cible = 18 
   
    etatPrecedent_up = GPIO.input(bouton_up) 
    etatPrecedent_down = GPIO.input(bouton_down) 

    print("Thermostat lancé ! Appuie sur UP (23) ou DOWN (24).")
    
    afficher_temperature(temperature_DHT, temperature_cible)

    while True:
        etat_up = GPIO.input(bouton_up)
        etat_down = GPIO.input(bouton_down)
      
        if etat_up != etatPrecedent_up:
            if etat_up == 0: 
                print("Bouton UP Appuyé ⬆️")
                temperature_cible += 1
                if temperature_cible >= 40:
                    temperature_cible = 40
                
                afficher_temperature(temperature_DHT, temperature_cible)        
            etatPrecedent_up = etat_up
        -
        if etat_down != etatPrecedent_down:
            if etat_down == 0:
                print("Bouton DOWN Appuyé ⬇️")
                temperature_cible -= 1
                if temperature_cible <= 0:
                    temperature_cible = 0
              
                afficher_temperature(temperature_DHT, temperature_cible)        
            etatPrecedent_down = etat_down

        t.sleep(0.05)

if __name__ == "__main__":
    try:
        test_boutons()
    except KeyboardInterrupt:
        print("\nFin du test")
        GPIO.cleanup()