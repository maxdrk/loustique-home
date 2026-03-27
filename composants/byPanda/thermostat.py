import time
import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemeThermostat:
    def __init__(self):
        self.capteur = Adafruit_DHT.DHT11
        self.pinDht = 22

        self.boutonPlus = 16
        self.boutonMoins = 18

        # display 4 digits
        # à brancher proprement quand le module exact sera fixé
        self.pinDisplayClk = 7
        self.pinDisplayDio = 11

        self.temperatureCible = 18
        self.temperatureReelle = None

        self.derniereLectureBouton = 0
        self.delaiLectureBouton = 0.25

        GPIO.setup(self.boutonPlus, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.boutonMoins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def lireTemperature(self):
        humidite, temperature = Adafruit_DHT.read_retry(self.capteur, self.pinDht)

        if temperature is None:
            print("Thermostat : lecture DHT11 impossible")
            return None

        return temperature

    def lireBoutons(self):
        maintenant = time.time()

        if maintenant - self.derniereLectureBouton < self.delaiLectureBouton:
            return

        if GPIO.input(self.boutonPlus):
            self.temperatureCible += 1
            self.derniereLectureBouton = maintenant
            print("Consigne :", self.temperatureCible, "°C")

        elif GPIO.input(self.boutonMoins):
            self.temperatureCible -= 1
            self.derniereLectureBouton = maintenant
            print("Consigne :", self.temperatureCible, "°C")

    def afficherTemperatures(self):
        # pour l'instant on affiche dans la console
        # le vrai code du display ira ici
        if self.temperatureReelle is None:
            print("Temp réelle : -- | cible :", self.temperatureCible)
        else:
            print("Temp réelle :", str(self.temperatureReelle) + "°C", "| cible :", str(self.temperatureCible) + "°C")

    def mettreAJour(self):
        self.lireBoutons()
        self.temperatureReelle = self.lireTemperature()
        self.afficherTemperatures()

        if self.temperatureReelle is None:
            return True

        return False

    def cleanup(self):
        # rien à éteindre ici, incroyable mais vrai
        pass
