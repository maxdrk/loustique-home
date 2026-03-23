from machine import  Pin

pir_sensor = Pin(33, Pin.IN)


def pir_detection():
    while True:
        if pir_sensor.value() == 1:
            led_bleue.on()
            utime.sleep(3)
            led_bleue.off()
        utime.sleep(0.1)
