import pymysql
import getpass
import bcrypt
from dotenv import load_dotenv
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


def login(username, password):
    conn = init()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        requete = "SELECT password FROM Auth WHERE username = %s"
        cursor.execute(requete, (username,))
        resultat = cursor.fetchone()
        if resultat and bcrypt.checkpw(password.encode('utf-8'), resultat[0].encode('utf-8')):
            print("Connexion réussie")
            log.info(f"Connexion réussie pour {username}")
            return True
        else:
            print("Identifiants incorrects")
            log.info("Identifiants incorrects,il est trop nul")
            return False
    except pymysql.err.OperationalError as e:
        print(f"Erreur : {e}")
        log.error(f"Erreur SQL : {e}")
        return False
    finally:
        cursor.close()
        conn.close()
def get_user_by_rfid(RFID):
    conn = init()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        requete = "SELECT username FROM Auth WHERE RFID = %s"
        cursor.execute(requete, (RFID))
        resultat = cursor.fetchone()
        
        if resultat:
            username = resultat[0]
            log.info(f"Badge RFID reconnu pour l'utilisateur : {username}")
            return username
        else:
            log.info(f"Tentative RFID refusée : badge {RFID} inconnu.")
            return None
            
    except pymysql.err.OperationalError as e:
        print(f"Erreur SQL RFID : {e}")
        log.error(f"Erreur SQL RFID : {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_users():
    conn = init()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, Fonctions, created_at FROM Auth")
        users = cursor.fetchall()
        return [{"username": u[0], "role": u[1], "created_at": str(u[2])} for u in users]
    except pymysql.err.OperationalError as e:
        log.error(f"Erreur get_users : {e}")
        return []
    finally:
        cursor.close()
        conn.close()        