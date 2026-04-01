import Adafruit_DHT as dht

# On définit juste le capteur et la broche (Rappel : 25 en BCM = broche physique 22)
capteur = dht.DHT11
pin = 25

def lire_temperature():
    humidite, temperature = dht.read_retry(capteur, pin)
    
    # On renvoie la température au script principal !
    if temperature is not None:
        return temperature
    else:
        return 0 # Sécurité si le capteur bugge, pour ne pas faire planter l'affichage