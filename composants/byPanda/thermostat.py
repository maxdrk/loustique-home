import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import tm1637

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemeThermostat:
    def __init__(self):
        self.capteur = Adafruit_DHT.DHT11
        self.pinDht = 25 # BCM 25 = BOARD 22

        self.boutonPlus = 16
        self.boutonMoins = 18

        # display 4 digits
        # à brancher proprement quand le module exact sera fixé
        self.pinDisplayClk = 7
        self.pinDisplayDio = 11

        self.temperatureCible = 18
        self.temperatureReelle = 99

        self.derniereLectureBouton = 0
        self.delaiLectureBouton = 0.25

        GPIO.setup(self.boutonPlus, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.boutonMoins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.display = tm1637.TM1637(clk=4, dio=17)
        self.display.brightness = 5
        self.display.show("----")

    def lireTemperature(self):
        humidite, temperature = Adafruit_DHT.read_retry(self.capteur, self.pinDht)

        if temperature is None:
            print("Thermostat : lecture DHT11 impossible")
            return 99
        return int(temperature)

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
    """
    def afficherTemperatures(self):
        # pour l'instant on affiche dans la console
        # le vrai code du display ira ici
        if self.temperatureReelle is None:
            print("Temp réelle : -- | cible :", self.temperatureCible)
        else:
            print("Temp réelle :", str(self.temperatureReelle) + "°C", "| cible :", str(self.temperatureCible) + "°C")
    """
    """            
    def valeurAffichee(self):
        if self.temperatureReelle is None:
            valeurReelle = 99
        else:
            valeurReelle = self.temperatureReelle
        return f"{valeurReelle:02d}{self.temperatureCible:02d}"
    """
    def valeurAffichee(self):
        return f"{self.temperatureReelle:02d}{self.temperatureCible:02d}"
    
    def afficherSurDisplay(self):
        valeur = self.valeurAffichee()
        self.display.show(valeur)

    def afficherConsole(self):
        print(
            "Temp réelle : ", str(self.temperatureReelle) + "°C",
            "| cible : ", str(self.temperatureCible) + "°C"
        )

    def mettreAJour(self):
        self.lireBoutons()
        self.temperatureReelle = self.lireTemperature()
        
        self.afficherConsole()
        self.afficherSurDisplay()
        return self.temperatureReelle == 99 # condition d'arrêt pour le test

    def cleanup(self):
        self.display.clear()
        pass
