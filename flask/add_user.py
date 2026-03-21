import pymysql
import getpass
import bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

def init():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET", "utf8mb4")
        )
        return conn

    except pymysql.err.OperationalError as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

def add():
    conn = init()
    if conn is None:
        return False

    username = input("Quel est l'username du nouvel utilisateur : ")
    password = getpass.getpass("Quel est le password : ")

    # Hashage du mot de passe avec bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor = conn.cursor()
        requete = "INSERT INTO Auth (username, password, created_at) VALUES (%s, %s, %s)"
        cursor.execute(requete, (username, hashed, datetime.now()))
        conn.commit()
        print(f"✅ Utilisateur '{username}' ajouté avec succès !")

    except pymysql.err.IntegrityError:
        print("❌ Cet utilisateur existe déjà")

    finally:
        cursor.close()
        conn.close()

add()
