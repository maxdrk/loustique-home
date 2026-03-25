"""
code adapté un une utilisation avec mcp3008 pour ldr

"""


import time
from gpiozero import LED, Button, PWMOutputDevice, AngularServo
from gpiozero import MCP3008  


led_verte = LED(12)
led_verte_luminosite = LED(25)
led_rouge = LED(13)
led_bleue = LED(14)
led_rouge_gas = LED(10)
servo = AngularServo(32, min_angle=0, max_angle=180)
pir_sensor = Button(33)
gas_sensor = Button(34)
buzzer = PWMOutputDevice(11)
ldr_sensor = MCP3008(channel=0) 


def activate_alarm():
    for _ in range(3):
        buzzer.value = 0.5
        time.sleep(0.5)
        buzzer.value = 0
        time.sleep(0.5)

def checkPin(guess):
    if guess == secret_pin:
        display_message("Code correct", guess)
        led_verte.on()
        servo.angle = 90
        time.sleep(2)
        servo.angle = 0
        led_verte.off()
    else:
        display_message("Code incorrect", guess)
        led_rouge.on()
        activate_alarm()
        time.sleep(2)
        led_rouge.off()

def pir_detection():
    while True:
        if pir_sensor.is_pressed:
            led_bleue.on()
            time.sleep(3)
            led_bleue.off()
        time.sleep(0.1)

def luminosite_detection():
    while True:
        luminosite = ldr_sensor.value * 1023
        print(luminosite)
        if luminosite > 300:
            led_verte_luminosite.on()
        else:
            led_verte_luminosite.off()
        time.sleep(0.5)

import threading
threading.Thread(target=pir_detection, daemon=True).start()
threading.Thread(target=luminosite_detection, daemon=True).start()