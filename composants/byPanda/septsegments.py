import tm1637
import time as t


display = tm1637.TM1637(clk=4, dio=17)
display.brightness(2)

def afficher_temperature(temperature):
    print(f"Test affichage: {temperature}")
    try:
        temp_entiere = int(temperature)
        texte_ecran = f"{temp_entiere} C" 
        display.show(texte_ecran)
        
    except Exception as e:
        print(f"Erreur d'affichage : {e}")