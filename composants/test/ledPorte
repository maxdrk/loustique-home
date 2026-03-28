import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ledPorte = 40

GPIO.setup(ledPorte, GPIO.OUT)

print("Test LED porte...")

try:
    while True:
        GPIO.output(ledPorte, GPIO.HIGH)
        print("LED ON")
        t.sleep(1)

        GPIO.output(ledPorte, GPIO.LOW)
        print("LED OFF")
        t.sleep(1)

except KeyboardInterrupt:
    print("Stop")

finally:
    GPIO.output(ledPorte, GPIO.LOW)