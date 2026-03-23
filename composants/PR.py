from machine import Pin,ADC


ldr_sensor_pin = 35
adc = ADC(Pin(ldr_sensor_pin))
adc.width(ADC.WIDTH_10BIT)
adc.atten(ADC.ATTN_11DB)

def luminosite_detection():
    while True:
        luminosite = adc.read()
        print (luminosite)
        if luminosite > 300:
            led_verte_luminosite.on()
        else:
            led_verte_luminosite.off()
        utime.sleep(0.5)
