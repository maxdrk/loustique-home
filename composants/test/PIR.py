import RPi.GPIO as GPIO
import time as t
##
GPIO.setmode(GPIO.BOARD)

pir = 10
GPIO.setup(pir, GPIO.IN)

print("Stabilisation...")
t.sleep(10)
print("Stabilisation terminée")

while True:
    print("PIR :", GPIO.input(pir))
    t.sleep(0.5)
