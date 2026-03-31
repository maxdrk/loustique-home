import time
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import urllib3

# On cache le gros texte d'avertissement orange (InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemePorteRFID:
    def __init__(self):
        """
        Initialise le système local d'accès par RFID.
        Gère le lecteur RFID et la LED de la porte.
        L'authentification est maintenant gérée par le serveur Flask et MariaDB.
        """
        self.pinLed = 40
        GPIO.setup(self.pinLed, GPIO.OUT, initial=GPIO.LOW)

        self.lecteur = SimpleMFRC522()

        self.badgeDetecte = None
        self.derniereOuverture = 0
        self.delaiEntreScans = 2

        # Ce thread sert à ne pas bloquer la boucle principale
        self.threadLecture = threading.Thread(target=self.boucleLectureRFID, daemon=True)
        self.threadLecture.start()

    def boucleLectureRFID(self):
        """
        Boucle secondaire qui attend les badges RFID.
        Utilise read_id() au lieu de read() pour éviter les erreurs "AUTH ERROR"
        sur la mémoire interne des badges.
        """
        while True:
            try:
                badgeId = self.lecteur.read_id()
                self.badgeDetecte = badgeId
            except Exception as erreur:
                print("Erreur RFID :", erreur)
                time.sleep(1)

    def ouvrirPorte(self):
        """Simule l'ouverture de la porte avec la LED pendant 2 secondes."""
        print("Porte ouverte.")
        GPIO.output(self.pinLed, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.pinLed, GPIO.LOW)

    def traiterBadge(self, badgeId):
        print(f"Badge détecté : {badgeId}")
        try:
            
            url = "https://127.0.0.1/rfid-scan" 
            donnees = {"badge_id": str(badgeId)}
            reponse = requests.post(url, json=donnees, timeout=2, verify=False)
            data = reponse.json()

            if data.get("success") is True:
                nom_utilisateur = data.get("username")
                print(f"Accès autorisé par la base de données pour : {nom_utilisateur}")
                self.ouvrirPorte()
            else:
                print("Accès refusé : ce badge n'est assigné à personne dans la base de données.")

        except Exception as e:
            print("Erreur de communication avec Flask :", e)

    def mettreAJour(self):
        """Fonction appelée en boucle dans le programme principal."""
        if self.badgeDetecte is None:
            return

        if time.time() - self.derniereOuverture < self.delaiEntreScans:
            return

        badgeId = self.badgeDetecte
        self.badgeDetecte = None
        self.derniereOuverture = time.time()

        self.traiterBadge(badgeId)

    def cleanup(self):
        """Eteint la LED de porte lors de la fermeture du programme."""
        GPIO.output(self.pinLed, GPIO.LOW)