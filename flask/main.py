from flask import Flask,render_template,request, jsonify
from bouton import led
import time
import os
import auth  
app = Flask(__name__)
@app.route("/")
def index():
    return  render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    succes = auth.login(data["username"], data["password"])
    if succes:
        return jsonify({"success": True, "message": "Connexion réussie"})
	
    else:
        return jsonify({"success": False, "message": "Identifiants incorrects"})
@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route("/led") 
def call_led():
	led()
	return "import bouton réussi" 	
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

