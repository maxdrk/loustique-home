import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SystemeAlarme:
    def __init__(self):
        """
        Initialise les composants liés à l'alarme.

        Cette classe gère uniquement la logique locale de sécurité :
        - le capteur PIR
        - le buzzer
        - la LED RGB de statut
        - le clavier 4x4

        Elle ne dépend d'aucune autre partie du projet.
        """

        # -----------------------------
        # Définition des pins physiques
        # -----------------------------
        self.pinPir = 10
        self.pinBuzzer = 12

        self.pinLedRouge = 11
        self.pinLedVerte = 13
        self.pinLedBleue = 15

        # Clavier 4x4
        # 4 lignes + 4 colonnes
        self.lignes = [29, 31, 33, 35]
        self.colonnes = [37, 32, 36, 38]

        # Disposition classique d'un clavier 4x4
        self.touches = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"]
        ]

        # -----------------------------
        # Variables de fonctionnement
        # -----------------------------
        self.codeSecret = "1234"
        self.codeSaisi = ""

        # Etats possibles :
        # - desarme
        # - arme
        # - alarme
        self.etat = "desarme"

        # Anti-rebond clavier
        self.derniereLecture = 0
        self.delaiLecture = 0.25

        self.initialiserGPIO()

        self.dernierEtatPir = 0

        print("Stabilisation du capteur PIR...")
        time.sleep(10)

        self.mettreAJourEtat()

    def initialiserGPIO(self):
        """Configure les broches du Raspberry Pi pour l'alarme."""
        GPIO.setup(self.pinPir, GPIO.IN)
        GPIO.setup(self.pinBuzzer, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.pinLedRouge, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pinLedVerte, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pinLedBleue, GPIO.OUT, initial=GPIO.LOW)

        for pin in self.lignes:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        for pin in self.colonnes:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def definirCouleur(self, rouge, vert, bleu):
        """
        Allume la LED RGB selon la couleur voulue.

        Paramètres :
        - rouge : True / False
        - vert  : True / False
        - bleu  : True / False
        """
        GPIO.output(self.pinLedRouge, GPIO.HIGH if rouge else GPIO.LOW)
        GPIO.output(self.pinLedVerte, GPIO.HIGH if vert else GPIO.LOW)
        GPIO.output(self.pinLedBleue, GPIO.HIGH if bleu else GPIO.LOW)

    def mettreAJourEtat(self):
        """
        Met à jour les sorties selon l'état actuel du système.

        - desarme : LED verte, buzzer éteint
        - arme    : LED bleue, buzzer éteint
        - alarme  : LED rouge, buzzer allumé
        """
        if self.etat == "desarme":
            self.definirCouleur(False, True, False)
            GPIO.output(self.pinBuzzer, GPIO.LOW)

        elif self.etat == "arme":
            self.definirCouleur(False, False, True)
            GPIO.output(self.pinBuzzer, GPIO.LOW)

        elif self.etat == "alarme":
            self.definirCouleur(True, False, False)
            GPIO.output(self.pinBuzzer, GPIO.HIGH)

    def armer(self):
        """Passe le système en mode armé."""
        self.etat = "arme"
        self.codeSaisi = ""
        self.mettreAJourEtat()
        print("Alarme activée.")

    def desarmer(self):
        """Passe le système en mode désarmé."""
        self.etat = "desarme"
        self.codeSaisi = ""
        self.mettreAJourEtat()
        print("Alarme désactivée.")

    def declencherAlarme(self):
        """
        Déclenche l'alarme si un mouvement est détecté alors
        que le système est armé.
        """
        if self.etat != "alarme":
            self.etat = "alarme"
            self.codeSaisi = ""
            self.mettreAJourEtat()
            print("Intrusion détectée : alarme déclenchée.")

    def lireClavier(self):
        """
        Scanne le clavier 4x4.

        Retour :
        - la touche détectée
        - None si aucune touche n'est pressée
        """
        maintenant = time.time()

        if maintenant - self.derniereLecture < self.delaiLecture:
            return None

        for indexLigne, ligne in enumerate(self.lignes):
            GPIO.output(ligne, GPIO.HIGH)

            for indexColonne, colonne in enumerate(self.colonnes):
                if GPIO.input(colonne) == GPIO.HIGH:
                    GPIO.output(ligne, GPIO.LOW)
                    self.derniereLecture = maintenant

                    # Petite attente pour éviter la lecture multiple
                    time.sleep(0.05)

                    return self.touches[indexLigne][indexColonne]

            GPIO.output(ligne, GPIO.LOW)

        return None

    def validerCode(self):
        """
        Vérifie le code saisi.

        Si le code est correct :
        - alarme désarmée -> armée
        - alarme armée    -> désarmée
        - alarme déclenchée -> désarmée

        Si le code est faux :
        - on efface la saisie
        """
        if self.codeSaisi == self.codeSecret:
            if self.etat == "desarme":
                self.armer()
            else:
                self.desarmer()
        else:
            print("Code incorrect.")
            self.codeSaisi = ""

    def traiterClavier(self, touche):
        """
        Gère la logique du clavier :
        - chiffres : ajout au code saisi
        - * : efface la saisie
        - # : valide le code
        """
        if touche is None:
            return

        print("Touche appuyée :", touche)

        if touche == "*":
            self.codeSaisi = ""
            print("Saisie effacée.")
            return

        if touche == "#":
            self.validerCode()
            return

        if touche.isdigit():
            if len(self.codeSaisi) < 8:
                self.codeSaisi += touche
                print("Code en cours :", "*" * len(self.codeSaisi))

    def surveillerPIR(self):
        """
        Vérifie le capteur de mouvement.

        Si un mouvement est détecté alors que l'alarme est armée,
        on passe en état d'alarme.
        """
        self.etatActuelPir = GPIO.input(self.pinPir)

        if self.etatActuelPir == GPIO.HIGH and self.dernierEtatPir == GPIO.LOW:
            print("Mouvement détecté par le PIR.")
            if self.etat == "arme":
                self.declencherAlarme()

        self.dernierEtatPir = self.etatActuelPir
        
    def mettreAJour(self):
        """
        Fonction appelée en boucle dans le programme principal.

        Elle :
        - lit le clavier
        - traite la touche appuyée
        - surveille le PIR
        - synchronise LED et buzzer avec l'état courant
        """
        touche = self.lireClavier()
        self.traiterClavier(touche)
        self.surveillerPIR()
        self.mettreAJourEtat()

    def cleanup(self):
        """
        Remet les sorties dans un état propre à la fermeture.
        """
        GPIO.output(self.pinBuzzer, GPIO.LOW)
        self.definirCouleur(False, False, False)
