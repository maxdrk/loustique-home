import Adafruit_DHT as dht
import time as t

capteur = dht.DHT11
pin = 22

while True:
    humidite, temperature = dht.read_retry(capteur, pin)

    if temperature is not None:
        print("Temp :", temperature, "°C")
    else:
        print("Erreur")

    t.sleep(2)