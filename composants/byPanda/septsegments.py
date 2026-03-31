import tm1637
import time as t

display = tm1637.TM1637(clk=4, dio=17)
display.brightness(2)

def afficher_temperature(temperature, temperature_moyenne):
    print(f"Test affichage: Cible {temperature} | Moyenne {temperature_moyenne}")
    try:
        temp1 = int(temperature)
        temp2 = int(temperature_moyenne)
        texte_ecran = f"{temp1:02d}{temp2:02d}" 
        
        display.show(texte_ecran)
        
    except Exception as e:
        print(f"Erreur d'affichage : {e}")