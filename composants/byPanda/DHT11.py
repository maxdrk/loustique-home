import Adafruit_DHT as dht
capteur = dht.DHT11
pin = 25

def lire_temperature():
    humidite, temperature = dht.read_retry(capteur, pin)
    if temperature is not None:
        return temperature
    else:
        return 0 