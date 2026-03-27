import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class EtatSysteme:
    def __init__(self):
        self.pinLedRouge = 35
        self.pinLedVerte = 37

        GPIO.setup(self.pinLedRouge, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pinLedVerte, GPIO.OUT, initial=GPIO.LOW)

    def signalerOk(self):
        GPIO.output(self.pinLedVerte, GPIO.HIGH)
        GPIO.output(self.pinLedRouge, GPIO.LOW)

    def signalerProbleme(self):
        GPIO.output(self.pinLedVerte, GPIO.LOW)
        GPIO.output(self.pinLedRouge, GPIO.HIGH)

    def cleanup(self):
        GPIO.output(self.pinLedRouge, GPIO.LOW)
        GPIO.output(self.pinLedVerte, GPIO.LOW)
