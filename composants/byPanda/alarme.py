import RPi.GPIO as GPIO
import time
import threading

# Configuration initiale
GPIO.setmode(GPIO.BOARD) # Utilisation des numéros physiques des pins
GPIO.setwarnings(False)

# --- CONFIGURATION PINS (BOARD) ---
PIN_LED_R  = 11
PIN_LED_G  = 15
PIN_LED_B  = 13
PIN_PIR    = 10
PIN_BUZZER = 12

# Pins Keypad (Vérifie bien tes branchements physiques sur ces numéros)
ROWS = [29, 31, 33, 35]        
COLS = [37, 32, 36, 38]          

KEYPAD_MAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D'],
]

CODE_SECRET = "1234"

# --- INITIALISATION GPIO ---
GPIO.setup(PIN_LED_R,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_G,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_B,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_PIR,    GPIO.IN)

for row in ROWS:
    GPIO.setup(row, GPIO.OUT, initial=GPIO.HIGH)
for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

etat_alarme = "Désarmée" 
etat_lock = threading.Lock()

_stop_buzzer   = threading.Event()
_thread_buzzer = None



def led(r=False, g=False, b=False):
    GPIO.output(PIN_LED_R, GPIO.HIGH if r else GPIO.LOW)
    GPIO.output(PIN_LED_G, GPIO.HIGH if g else GPIO.LOW)
    GPIO.output(PIN_LED_B, GPIO.HIGH if b else GPIO.LOW)

def led_bleu():  led(b=True)
def led_vert():  led(g=True)
def led_rouge(): led(r=True)
def led_off():   led()

def bip(nb=1, duree=0.08, pause=0.12):
    for _ in range(nb):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(duree)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(pause)

def _buzzer_continu(stop_event: threading.Event):
    while not stop_event.is_set():
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(PIN_BUZZER, GPIO.LOW)


def lire_touche():

    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.LOW)
        time.sleep(0.01) # Stabilisation électrique
        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                time.sleep(0.05) # Anti-rebond
                while GPIO.input(col) == GPIO.LOW:
                    time.sleep(0.01) 
                GPIO.output(row, GPIO.HIGH)
                return KEYPAD_MAP[i][j]
        GPIO.output(row, GPIO.HIGH)
    return None

def lire_code(nb_chiffres=4, timeout=20):
    saisi = ""
    debut  = time.time()
    print("  Entrez le code : ", end="", flush=True)
    while len(saisi) < nb_chiffres:
        if time.time() - debut > timeout:
            print("\n  [Timeout]")
            return ""
        touche = lire_touche()
        if touche and touche.isdigit():
            saisi += touche
            bip(1, 0.05) # Petit bip de confirmation touche
            print("*", end="", flush=True)
        time.sleep(0.05)
    print()
    return saisi

# --- GESTION DES ÉTATS ---

def passer_en_desarmee():
    global etat_alarme, _thread_buzzer
    _stop_buzzer.set()
    if _thread_buzzer and _thread_buzzer.is_alive():
        _thread_buzzer.join()
    with etat_lock:
        etat_alarme = "Désarmée"
    led_bleu()
    print("[ÉTAT] ● DÉSARMÉE")

def passer_en_armee():
    global etat_alarme
    with etat_lock:
        etat_alarme = "Armée"
    led_vert()
    bip(nb=2)
    print("[ÉTAT] ● ARMÉE")

def passer_en_declenchee():
    global etat_alarme, _thread_buzzer
    with etat_lock:
        # On ne déclenche que si on était armé
        if etat_alarme == "Armée":
            etat_alarme = "Déclenchée"
            led_rouge()
            print("[ÉTAT] ● DÉCLENCHÉE !")
            _stop_buzzer.clear()
            _thread_buzzer = threading.Thread(target=_buzzer_continu, args=(_stop_buzzer,), daemon=True)
            _thread_buzzer.start()

# --- SURVEILLANCE ---

def _surveiller_pir(stop_evt: threading.Event):
    while not stop_evt.is_set():
        with etat_lock:
            local_etat = etat_alarme
        if local_etat == "Armée" and GPIO.input(PIN_PIR) == GPIO.HIGH:
            passer_en_declenchee()
        time.sleep(0.2)

def boucle_principale():
    """Lancée par board1main dans un thread."""
    passer_en_desarmee()
    
    stop_pir = threading.Event()
    thread_pir = threading.Thread(target=_surveiller_pir, args=(stop_pir,), daemon=True)
    thread_pir.start()

    print("\n=== Système d'alarme démarré ===")

    try:
        while True:
            with etat_lock:
                current = etat_alarme

            # CAS 1 : L'alarme est éteinte, on attend le code pour l'allumer
            if current == "Désarmée":
                print("  [DÉSARMÉE] Entrez code pour ARMER...")
                code = lire_code(len(CODE_SECRET))
                if code == CODE_SECRET:
                    passer_en_armee()
                elif code != "":
                    bip(1, 0.5)

            # CAS 2 : L'alarme est allumée, on attend le code pour l'éteindre
            elif current == "Armée":
                # On réutilise lire_code ici pour permettre le désarmement manuel
                print("  [ARMÉE] Entrez code pour DÉSARMER...")
                code = lire_code(len(CODE_SECRET))
                if code == CODE_SECRET:
                    passer_en_desarmee()
                elif code != "":
                    bip(1, 0.5)

            # CAS 3 : L'alarme sonne, on attend le code pour stopper le buzzer
            elif current == "Déclenchée":
                print("  [ALERTE] Entrez code pour STOPPER...")
                code = lire_code(len(CODE_SECRET))
                if code == CODE_SECRET:
                    passer_en_desarmee()
            
            time.sleep(0.1)
    finally:
        stop_pir.set()
        _stop_buzzer.set()
        led_off()