import os
import sys
from fastapi import FastAPI
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
composants = os.path.join(BASE_DIR, "composants", "byPanda")
sys.path.insert(0, composants) 

#from lumieres import SystemeLumieres
from thermostat import SystemeThermostat
#from volets import SystemeVolets
from septsegments import afficher_temperature 

app = FastAPI(title="Loustiques API - Pi 2")

#controleur_lumieres = SystemeLumieres()
controleur_thermostat = SystemeThermostat()
#controleur_volet = SystemeVolets()
"""
@app.get("/up_led")
async def allumer_led():
    controleur_lumieres.allumerLumieres()
    controleur_lumieres.modeManuel = True 
    return {"success": True, "message": "Lumière allumée par le Pi 2"}
    
@app.get("/down_led")
async def eteindre_led():
    controleur_lumieres.eteindreLumieres()
    controleur_lumieres.modeManuel = True 
    return {"success": True, "message": "Lumière éteinte par le Pi 2"}
"""
@app.get("/temperature")
async def read_temp():
    temp = controleur_thermostat.lireTemperature()
    if temp is None:
        return {"success": False, "message": "Impossible de lire le capteur DHT11"}
    afficher_temperature(temp)
    return {"success": True, "temperature": temp}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
