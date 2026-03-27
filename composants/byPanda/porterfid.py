import time
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemePorteRFID:
    def __init__(self):
        """
        Initialise le système local d'accès par RFID.

        Cette classe gère uniquement :
        - le lecteur RFID
        - la LED qui symbolise l'ouverture de porte

        Elle ne pilote pas l'alarme et ne dépend pas du site web.
        """
        self.pinLed = 40
        GPIO.setup(self.pinLed, GPIO.OUT, initial=GPIO.LOW)

        self.lecteur = SimpleMFRC522()

        # Remplacer ces identifiants par les vrais UID autorisés
        self.badgesAutorises = {
            123456789012: "Admin",
            987654321098: "Utilisateur"
        }

        self.badgeDetecte = None
        self.derniereOuverture = 0
        self.delaiEntreScans = 2

        # Ce thread sert à ne pas bloquer la boucle principale
        # pendant l'attente d'un badge RFID.
        self.threadLecture = threading.Thread(target=self.boucleLectureRFID, daemon=True)
        self.threadLecture.start()

    def boucleLectureRFID(self):
        """
        Boucle secondaire qui attend les badges RFID.

        La méthode read() est bloquante selon la bibliothèque utilisée,
        donc on la place dans un thread séparé pour que le reste du
        programme continue de tourner normalement.
        """
        while True:
            try:
                badgeId, _ = self.lecteur.read()
                self.badgeDetecte = badgeId
            except Exception as erreur:
                print("Erreur RFID :", erreur)
                time.sleep(1)

    def badgeAutorise(self, badgeId):
        """Retourne True si le badge est autorisé."""
        return badgeId in self.badgesAutorises

    def ouvrirPorte(self):
        """
        Simule l'ouverture de la porte avec la LED.

        Ici la LED reste allumée 2 secondes pour représenter
        l'accès autorisé.
        """
        print("Porte ouverte.")
        GPIO.output(self.pinLed, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.pinLed, GPIO.LOW)

    def traiterBadge(self, badgeId):
        """
        Vérifie si le badge présenté est autorisé.
        Si oui, on ouvre la porte.
        Sinon, on affiche un refus.
        """
        print("Badge détecté :", badgeId)

        if self.badgeAutorise(badgeId):
            print("Accès autorisé pour", self.badgesAutorises[badgeId])
            self.ouvrirPorte()
        else:
            print("Accès refusé.")

    def mettreAJour(self):
        """
        Fonction appelée en boucle dans le programme principal.

        Elle récupère le dernier badge lu par le thread RFID
        et le traite si nécessaire.
        """
        if self.badgeDetecte is None:
            return

        if time.time() - self.derniereOuverture < self.delaiEntreScans:
            return

        badgeId = self.badgeDetecte
        self.badgeDetecte = None
        self.derniereOuverture = time.time()

        self.traiterBadge(badgeId)

    def cleanup(self):
        """
        Eteint la LED de porte lors de la fermeture du programme.
        """
        GPIO.output(self.pinLed, GPIO.LOW)
