import tm1637
import time as t
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

display = tm1637.TM1637(clk=7, dio=11)

display.brightness(2)

print("Test affichage...")

try:
    while True:
        display.show("1234")
        print("1234")
        t.sleep(2)

        display.show("0000")
        print("0000")
        t.sleep(2)

except KeyboardInterrupt:
    display.show("----")
    print("Stop")