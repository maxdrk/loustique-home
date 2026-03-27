import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemeLumieres:
    def __init__(self):
        # la pin de la 2e photorésistance manque sur le schéma
        # donc ici on met une valeur temporaire
        # elle apparaîtra peut-être un jour, comme la motivation en fin de projet
        self.pinPhotoInterieure = 29

        self.led1 = 21
        self.led2 = 31
        self.led3 = 33

        self.boutonManuel = 36

        self.modeManuel = False
        self.lumieresAllumees = False

        GPIO.setup(self.pinPhotoInterieure, GPIO.IN)
        GPIO.setup(self.led1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.led2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.led3, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.boutonManuel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.derniereLectureBouton = 0
        self.delaiLectureBouton = 0.25

    def lireLuminositeInterieure(self):
        return GPIO.input(self.pinPhotoInterieure)

    def allumerLumieres(self):
        GPIO.output(self.led1, GPIO.HIGH)
        GPIO.output(self.led2, GPIO.HIGH)
        GPIO.output(self.led3, GPIO.HIGH)
        self.lumieresAllumees = True

    def eteindreLumieres(self):
        GPIO.output(self.led1, GPIO.LOW)
        GPIO.output(self.led2, GPIO.LOW)
        GPIO.output(self.led3, GPIO.LOW)
        self.lumieresAllumees = False

    def gererBoutonManuel(self):
        maintenant = time.time()

        if maintenant - self.derniereLectureBouton < self.delaiLectureBouton:
            return

        if GPIO.input(self.boutonManuel):
            self.modeManuel = not self.modeManuel
            self.derniereLectureBouton = maintenant

            if self.modeManuel:
                self.lumieresAllumees = not self.lumieresAllumees

                if self.lumieresAllumees:
                    self.allumerLumieres()
                else:
                    self.eteindreLumieres()
            else:
                print("Lumières : retour en auto")

    def mettreAJour(self):
        self.gererBoutonManuel()

        if self.modeManuel:
            return False

        luminosite = self.lireLuminositeInterieure()

        if luminosite == 0:
            self.allumerLumieres()
            print("Lumières : on allume")
        else:
            self.eteindreLumieres()
            print("Lumières : on coupe")

        return False

    def cleanup(self):
        self.eteindreLumieres()
