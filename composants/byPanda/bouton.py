import RPi.GPIO as GPIO
import time as t
from septsegments import afficher_temperature
from DHT11 import lire_temperature

# --- Configuration des Pins ---
bouton_up = 23
bouton_down = 24 

# --- Variables Globales Partagées ---
temperature_cible = 18 

def setup_boutons():
    """Initialisation des GPIO (à appeler au début)"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bouton_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(bouton_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test_boutons():

    global temperature_cible 
    setup_boutons()

    temperature_DHT = lire_temperature()
    etatPrecedent_up = GPIO.input(bouton_up)
    etatPrecedent_down = GPIO.input(bouton_down)

    print(f"Thermostat lancé ! Cible actuelle : {temperature_cible}°C")
    
    while True:
        etat_up = GPIO.input(bouton_up)
        etat_down = GPIO.input(bouton_down)
      
        if etat_up == 0 and etatPrecedent_up == 1: 
            temperature_cible = min(40, temperature_cible + 1)
            print(f"Bouton UP -> Nouvelle cible : {temperature_cible}")
            afficher_temperature(lire_temperature(), temperature_cible)        
        
        if etat_down == 0 and etatPrecedent_down == 1:
            temperature_cible = max(0, temperature_cible - 1)
            print(f"Bouton DOWN -> Nouvelle cible : {temperature_cible}")
            afficher_temperature(lire_temperature(), temperature_cible)        

        etatPrecedent_up = etat_up
        etatPrecedent_down = etat_down
        t.sleep(0.05)