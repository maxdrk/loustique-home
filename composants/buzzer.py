from machine import Pin,PWM

buzzer_pin = 11

buzzer = PWM(Pin(buzzer_pin), freq=440, duty=0)

def activate_alarm():
    for _ in range(3):
        buzzer.duty(512)
        utime.sleep(0.5)
        buzzer.duty(0)
        utime.sleep(0.5)

