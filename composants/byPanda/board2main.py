import time
from thermostat import SystemeThermostat
from lumieres import SystemeLumieres
from volets import SystemeVolets
from etatsysteme import EtatSysteme

thermostat = SystemeThermostat()
lumieres = SystemeLumieres()
volets = SystemeVolets()
etat = EtatSysteme()

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
