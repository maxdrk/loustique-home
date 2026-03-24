import pymysql
import getpass
import bcrypt
from dotenv import load_dotenv
from datetime import datetime
import os
from log import log

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
        print(f"Erreur de connexion : {e}")
        log.error(f"Erreur de connexion : {e}")
        return None

def add_user(username, password, role):
    conn = init()
    if conn is None:
        return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    

    try:
        cursor = conn.cursor()
        requete = "INSERT INTO Auth (username, password, Fonctions, created_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(requete, (username, hashed, role, datetime.now()))
        conn.commit()
        log.info(f"Utilisateur '{username}' ({role}) ajouté")
        return True
    except pymysql.err.IntegrityError:
        log.error(f"Utilisateur existant : {username}")
        return False
    finally:
        cursor.close()
        conn.close()