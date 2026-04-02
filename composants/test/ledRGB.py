import RPi.GPIO as GPIO
import time as t
##
GPIO.setmode(GPIO.BOARD)

r, g, b = 11, 13, 15

GPIO.setup(r, GPIO.OUT)
GPIO.setup(g, GPIO.OUT)
GPIO.setup(b, GPIO.OUT)

while True:
    GPIO.output(r, 1); t.sleep(1); GPIO.output(r, 0)
    GPIO.output(g, 1); t.sleep(1); GPIO.output(g, 0)
    GPIO.output(b, 1); t.sleep(1); GPIO.output(b, 0)
