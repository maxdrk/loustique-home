from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys




app = FastAPI(title="Loustiques API - Pi 2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
composants = os.path.join(BASE_DIR, "composants", "byPanda")
sys.path.insert(0, composants) 
from lumieres import SystemeLumieres


class CommandeLumiere(BaseModel):
    action: str

@app.post("/Lumière")
async def action_pi2(commande: CommandeLumiere):
    if commande.action == "allumer_lumiere":
        return {"success": True, "message": "Lumière allumée par le Pi 2"}
    
    return {"success": False, "message": "Action inconnue"}