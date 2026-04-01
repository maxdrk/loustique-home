from flask import Flask, render_template, request, jsonify
from flask_talisman import Talisman
from led import led
import os
import sys
import log
from add_user import add_user
import auth
import re

app = Flask(__name__)
Talisman(app, force_https=True,
content_security_policy=False)
current_user = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
composants = os.path.join(BASE_DIR, "composants", "byPanda")
sys.path.insert(0, composants)  
from alarme import SystemeAlarme
from lumieres import SystemeLumieres
from board1main import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    global current_user
    data = request.get_json()
    succes = auth.login(data["username"], data["password"])
    if succes:
        current_user = data["username"]
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/led", methods=["POST"])
def call_led():
    etat = SystemeLumieres.mettreAJourEtat() 
    if (etat == 0):
        SystemeLumieres.allumerLumieres
    
    else:
        SystemeLumieres.eteindreLumieres()  
    return jsonify({"success": True})
# Variable temporaire pour stocker le dernier badge scanné
dernier_badge_scanne = None

@app.route("/rfid-scan", methods=["POST"])
def rfid_scan():
    global dernier_badge_scanne
    data = request.get_json()
    badge_id = data.get("badge_id")
    
    # On va créer cette fonction dans ton fichier auth.py juste après
    username = auth.get_user_by_rfid(badge_id)
    
    if username:
        # Le badge est dans la base de données ! On autorise.
        dernier_badge_scanne = username
        return jsonify({"success": True, "username": username})
    else:
        # Badge inconnu
        return jsonify({"success": False})

@app.route("/check-rfid-login", methods=["GET"])
def check_rfid_login():
    global dernier_badge_scanne
    global current_user
    
    # Si le Raspberry Pi a signalé un badge validé récemment
    if dernier_badge_scanne:
        user = dernier_badge_scanne
        
        # On valide la connexion côté serveur
        current_user = user 
        
        # On vide la variable pour ne pas le reconnecter en boucle à l'infini
        dernier_badge_scanne = None 
        
        return jsonify({"success": True, "username": user})
    
    return jsonify({"success": False})

              

@app.route("/alarme",methods=["POST"])
def armer_alarme():
    SystemeAlarme.armer()
    return jsonify({"success": True})

     
   

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/admin/logs")
def logs_page():
    return render_template("log.html")


@app.route("/admin/logs/data")
def get_logs():
    try:
        with open('/var/log/loustique.log', 'r') as f:
            lines = f.readlines()
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        lines = [ansi_escape.sub('', line) for line in lines[-200:]]
        return jsonify({"success": True, "logs": lines})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route("/admin/add_user",methods=["POST"])
@app.route("/admin/add_user", methods=["POST"])
def create_user():  
    data = request.get_json()
    succes = add_user(data["username"], data["password"], data["role"])
    if succes:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Utilisateur déjà existant"})
@app.route("/admin/get_users")
def get_users():
    users = auth.get_users()
    return jsonify({"success": True, "users": users})

@app.route("/api/relais-pi2/<action>", methods=["GET"])
def relais_pi2(action):
    """
    Flask sert de relais. Le navigateur demande à Flask, et Flask demande au Pi 2.
    """
    try:
        # L'adresse de ton Pi 2
        url_pi2 = f"https://pi32.local:8000/{action}" 
        
        # Le Pi 1 fait la requête ! verify=False permet d'ignorer le faux certificat
        reponse = requests.get(url_pi2, timeout=5, verify=False)
        
        return jsonify(reponse.json())
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    print("[*] Démarrage du lecteur RFID et de l'alarme en arrière-plan...")
    thread_hardware = threading.Thread(target=call_board1, daemon=True)
    thread_hardware.start()
    app.run(
        host="0.0.0.0",
        port=443,
        ssl_context=(
            os.path.join(BASE_DIR, 'web_secu', 'ssl', 'cert.pem'),
            os.path.join(BASE_DIR, 'web_secu', 'ssl', 'key.pem')
        )
    )