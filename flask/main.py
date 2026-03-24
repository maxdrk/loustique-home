from flask import Flask, render_template, request, jsonify
from led import led
import os
from add_user import add_user
import auth
import re

app = Flask(__name__)

current_user = None

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
    led(current_user)
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

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        ssl_context=(
            os.path.join(BASE_DIR, 'web_secu', 'ssl', 'cert.pem'),
            os.path.join(BASE_DIR, 'web_secu', 'ssl', 'key.pem')
        )
    )