import RPi.GPIO as GPIO
import time as t


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1 = 9
led2 = 6 
led3 = 13  # example BCM pin

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

print("Test LEDs...")

try:
    while True:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.HIGH)
        print("LED ON")
        t.sleep(1)

        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)
        print("LED OFF")
        t.sleep(1)

except KeyboardInterrupt:
    print("Stop")

finally:
    GPIO.cleanup()