import time
from thermostat import SystemeThermostat as thermostat
from lumieres import SystemeLumieres as lumieres
from volets import SystemeVolets as volets
from etatsysteme import EtatSysteme as etat

try:
    while True:
        erreurThermostat = thermostat.mettreAJour()
        erreurLumieres = lumieres.mettreAJour()
        erreurVolets = volets.mettreAJour()

        if erreurThermostat or erreurLumieres or erreurVolets:
            etat.signalerProbleme()
        else:
            etat.signalerOk()

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nArrêt du programme.")

finally:
    thermostat.cleanup()
    lumieres.cleanup()
    volets.cleanup()
    etat.cleanup()
