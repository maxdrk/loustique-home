import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemeVolets:
    def __init__(self):
        self.pinPhotoExterieure = 32
        self.pinServo = 12
        self.boutonManuel = 13

        self.modeManuel = False
        self.voletsOuverts = True

        GPIO.setup(self.pinPhotoExterieure, GPIO.IN)
        GPIO.setup(self.pinServo, GPIO.OUT)
        GPIO.setup(self.boutonManuel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.pwm = GPIO.PWM(self.pinServo, 50)
        self.pwm.start(0)

        self.derniereLectureBouton = 0
        self.delaiLectureBouton = 0.25

    def ouvrirVolets(self):
        self.pwm.ChangeDutyCycle(7)
        self.voletsOuverts = True
        print("Volets : ouverts")

    def fermerVolets(self):
        self.pwm.ChangeDutyCycle(2)
        self.voletsOuverts = False
        print("Volets : fermés")

    def gererBoutonManuel(self):
        maintenant = time.time()

        if maintenant - self.derniereLectureBouton < self.delaiLectureBouton:
            return

        if GPIO.input(self.boutonManuel):
            self.derniereLectureBouton = maintenant

            if self.voletsOuverts:
                self.fermerVolets()
            else:
                self.ouvrirVolets()

            self.modeManuel = True
            print("Volets : mode manuel")

    def lireLuminositeExterieure(self):
        return GPIO.input(self.pinPhotoExterieure)

    def mettreAJour(self):
        self.gererBoutonManuel()

        if self.modeManuel:
            return False

        luminosite = self.lireLuminositeExterieure()

        if luminosite == 1:
            self.fermerVolets()
        else:
            self.ouvrirVolets()

        return False

    def cleanup(self):
        self.pwm.stop()
