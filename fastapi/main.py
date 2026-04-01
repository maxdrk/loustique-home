import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import RPi.GPIO as GPIO 
import uvicorn

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
composants = os.path.join(BASE_DIR, "composants", "byPanda")
sys.path.insert(0, composants) 

from lumieres import SystemeLumieres
from thermostat import SystemeThermostat
#from volets import SystemeVolets
from etatsysteme import EtatSysteme
from septsegments import afficher_temperature 

app = FastAPI(title="L'API des loustiques")

controleur_lumieres = SystemeLumieres()
controleur_thermostat = SystemeThermostat()
#controleur_volet = SystemeVolets()
etatSysteme = EtatSysteme()

@app.get("/up_led")
async def allumer_led():
    try:
        controleur_lumieres.allumerLumieres()
        controleur_lumieres.modeManuel = True 
        etatSysteme.signalerOk()
        return {"success": True, "message": "Lumière allumée par le Pi 2"}
        
    except Exception as e:  
        etatSysteme.signalerProbleme()
        return {"success": False, "message": str(e)}  
    
@app.get("/down_led")
async def eteindre_led():
    try:
        controleur_lumieres.eteindreLumieres()
        controleur_lumieres.modeManuel = True 
        etatSysteme.signalerOk()
        return {"success": True, "message": "Lumière éteinte par le Pi 2"}
        
    except Exception as e:
        etatSysteme.signalerProbleme()
        return {"success": False, "message": str(e)}  

@app.get("/temperature")
async def read_temp():
    try:
        temp = controleur_thermostat.lireTemperature()
        if temp is None:
            etatSysteme.signalerProbleme() 
            return {"success": False, "message": "Impossible de lire le capteur DHT11"}
            
        etatSysteme.signalerOk()
        afficher_temperature(temp, 18)
        return {"success": True, "temperature": temp}
        
    except Exception as e: 
        etatSysteme.signalerProbleme()
        return {"success": False, "message": str(e)}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise tous les sites web (le fameux "*")
    allow_credentials=False, # (Doit être False quand on met "*")
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les en-têtes
)        
            
if __name__ == "__main__":
    # On prépare les chemins proprement pour éviter les erreurs de parenthèses
    # (Vérifie bien que le dossier 'web_secu' est bien dans le dossier racine de ton Pi 2)
    chemin_cle = os.path.join(BASE_DIR, 'web_secu', 'ssl', 'key.pem')
    chemin_cert = os.path.join(BASE_DIR, 'web_secu', 'ssl', 'cert.pem')
    
    # On lance Uvicorn avec la bonne syntaxe
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        ssl_keyfile=chemin_cle,
        ssl_certfile=chemin_cert
    )