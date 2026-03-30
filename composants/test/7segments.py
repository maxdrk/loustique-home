import tm1637
import time as t

# attention : mode BOARD
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