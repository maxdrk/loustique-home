import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BOARD)

servo = 12
GPIO.setup(servo, GPIO.OUT)

pwm = GPIO.PWM(servo, 50)
pwm.start(0)

while True:
    print("Position 1")
    pwm.ChangeDutyCycle(2)
    t.sleep(2)

    print("Position 2")
    pwm.ChangeDutyCycle(7)
    t.sleep(2)