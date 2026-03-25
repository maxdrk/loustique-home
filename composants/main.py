import time
from machine import I2C, Pin, PWM, ADC
import utime




pwm = PWM(Pin(32), freq=50)

led_verte = Pin(12, Pin.OUT)
led_verte_luminosite = Pin(25, Pin.OUT)
led_rouge = Pin(13, Pin.OUT)
led_bleue = Pin(14, Pin.OUT)
led_rouge_gas = Pin(10, Pin.OUT)

pir_sensor = Pin(33, Pin.IN)
gas_sensor = Pin(34, Pin.IN)
ldr_sensor_pin = 35

adc = ADC(Pin(ldr_sensor_pin))
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)

buzzer_pin = 11

buzzer = PWM(Pin(buzzer_pin), freq=440, duty=0)

def activate_alarm():
    for _ in range(3):
        buzzer.duty(512)
        utime.sleep(0.5)
        buzzer.duty(0)
        utime.sleep(0.5)

def checkPin(guess):
    if guess == secret_pin:
        display_message("Code correct")
        led_verte.on()
        pwm.duty(120)
        utime.sleep(2)
        pwm.duty(75)
        led_verte.off()
    else:
        display_message("Code incorrect")
        led_rouge.on()
        activate_alarm()
        utime.sleep(2)
        led_rouge.off()

def display_message(message):
    oled.fill(0)
    hidden_secret = '*' * len(guess)
    oled.text(hidden_secret, 0, 0)
    oled.show()
    utime.sleep(1)
    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

def pir_detection():
    while True:
        if pir_sensor.value() == 1:
            led_bleue.on()
            utime.sleep(3)
            led_bleue.off()
        utime.sleep(0.1)


def luminosite_detection():
    while True:
        luminosite = adc.read()
        print (luminosite)
        if luminosite > 300:
            led_verte_luminosite.on()
        else:
            led_verte_luminosite.off()
        utime.sleep(0.5)

import _thread
_thread.start_new_thread(pir_detection, ())
_thread.start_new_thread(luminosite_detection, ())
