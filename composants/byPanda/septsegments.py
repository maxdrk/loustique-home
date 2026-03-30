import tm1637
import time as t

# attention : mode BOARD
display = tm1637.TM1637(clk=4, dio=17)

display.brightness = 5


def afficher_temperature(temperature):
    print("Test affichage...")


    try:
        while True:
            display.show(temperature)
            print(temperature)
            t.sleep(2)

    except KeyboardInterrupt:
        display.show("----")
        print("Stop")