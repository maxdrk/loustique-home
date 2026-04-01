import tm1637
import time as t

_display = None

def get_display():
    global _display
    if _display is None:
        _display = tm1637.TM1637(clk=4, dio=17)
        _display.brightness(2)
    return _display

def afficher_temperature(temperature, temperature_moyenne):
    print(f"Test affichage: Cible {temperature} : Moyenne {temperature_moyenne}")
    try:
        temp1 = int(temperature)
        temp2 = int(temperature_moyenne)
        
        disp = get_display()
        
   
        texte_ecran = f"{temp1:02d}{temp2:02d}" 
 
        if hasattr(disp, 'show_doublepoint'):
            disp.show_doublepoint(True)
        elif hasattr(disp, 'point'):
            disp.point(True)
        
        disp.show(texte_ecran)
        
    except Exception as e:
        print(f"Erreur d'affichage : {e}")