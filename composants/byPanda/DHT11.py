import Adafruit_DHT as dht
import time as t
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
capteur = dht.DHT11
pin = 25

def lire_temperature():
    humidite, temperature = dht.read_retry(capteur, pin)

    if temperature is not None:
        print("Temp :", temperature, "°C")
    else:
        print("Erreur")

    t.sleep(2)

lire_temperature()
