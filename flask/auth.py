import pymysql
import getpass
import bcrypt
from dotenv import load_dotenv
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

def login(username,password):
    #username = input("Username : ")
    #password = getpass.getpass("Mot de passe : ")

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
            return True
        else:
            print(" Identifiants incorrects")
            return False

    except pymysql.err.OperationalError as e:
        print(f"Erreur : {e}")
        return False

    finally:
        cursor.close()
        conn.close()


