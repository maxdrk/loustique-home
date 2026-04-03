import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN_LED_R  = 17
PIN_LED_G  = 22
PIN_LED_B  = 3
PIN_PIR    = 23
PIN_BUZZER = 18

ROWS = [5, 6, 13, 19]        
COLS = [26, 12, 16, 20]      

KEYPAD_MAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D'],
]

CODE_SECRET = "1234"


GPIO.setup(PIN_LED_R,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_G,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_B,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_PIR,    GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for row in ROWS:
    GPIO.setup(row, GPIO.OUT, initial=GPIO.HIGH)
for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

etat = "Désarmée"
etat_lock = threading.Lock()

_stop_buzzer   = threading.Event()
_thread_buzzer = None



def led(r=False, g=False, b=False):
    GPIO.output(PIN_LED_R, GPIO.HIGH if r else GPIO.LOW)
    GPIO.output(PIN_LED_G, GPIO.HIGH if g else GPIO.LOW)
    GPIO.output(PIN_LED_B, GPIO.HIGH if b else GPIO.LOW)

def bip(nb=1, duree=0.08, pause=0.12):
    for _ in range(nb):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(duree)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(pause)

def _buzzer_continu(stop_event):
    while not stop_event.is_set():
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(PIN_BUZZER, GPIO.LOW)

def etat_alarme(): 
    with etat_lock:
        return etat


def lire_touche():
    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.LOW)
        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                time.sleep(0.05)               
                while GPIO.input(col) == GPIO.LOW:
                    pass                  
                GPIO.output(row, GPIO.HIGH)
                return KEYPAD_MAP[i][j]
        GPIO.output(row, GPIO.HIGH)
    return None

def lire_code(nb_chiffres=4, timeout=30):
    saisi = ""
    debut  = time.time()
    print("  Code : ", end="", flush=True)
    while len(saisi) < nb_chiffres:
        if time.time() - debut > timeout:
            print("\n  [Timeout]")
            return ""
        touche = lire_touche()
        if touche and touche.isdigit():
            saisi += touche
            print("*", end="", flush=True)
        time.sleep(0.05)
    print()
    return saisi


def passer_en_desarmee():
    global etat, _thread_buzzer
    _stop_buzzer.set()
    if _thread_buzzer and _thread_buzzer.is_alive():
        _thread_buzzer.join()
    with etat_lock:
        etat = "Désarmée"
    led(b=True) # Bleu
    print("[ÉTAT] ● DÉSARMÉE")

def passer_en_armee():
    global etat
    print("[ÉTAT] ● ARMEMENT... Stabilisation capteur (10s)")
    led(r=True, g=True) 
    time.sleep(10)
    
    with etat_lock:
        etat = "Armée"
    led(g=True) 
    bip(nb=2)               
    print("[ÉTAT] ● ARMÉE — Surveillance active !")

def passer_en_declenchee():
    global etat, _thread_buzzer
    with etat_lock:
        etat = "Déclenchée"
    led(r=True) # Rouge
    print("[ÉTAT] ● DÉCLENCHÉE !")
    _stop_buzzer.clear()
    _thread_buzzer = threading.Thread(target=_buzzer_continu, args=(_stop_buzzer,), daemon=True)
    _thread_buzzer.start()

def _surveiller_pir(stop_evt):
    print("[PIR] Thread de surveillance prêt")
    while not stop_evt.is_set():
        with etat_lock:
            etat_local = etat
        
        if etat_local == "Armée":
            if GPIO.input(PIN_PIR) == GPIO.HIGH:
                time.sleep(0.3)
                if GPIO.input(PIN_PIR) == GPIO.HIGH:
                    passer_en_declenchee()
        
        time.sleep(0.1)


def boucle_principale():
    passer_en_desarmee()

    stop_pir   = threading.Event()
    thread_pir = threading.Thread(target=_surveiller_pir, args=(stop_pir,), daemon=True)
    thread_pir.start()

    print("\n=== Système prêt (Code: " + CODE_SECRET + ") ===")

    try:
        while True:
            etat_actuel = etat_alarme()

            if etat_actuel == "Désarmée":
                print("→ Saisir code pour ARMER :")
                if lire_code() == CODE_SECRET:
                    passer_en_armee()

            elif etat_actuel == "Armée":
                print("→ Système ARMÉ (Code pour DÉSARMER) :")
                if lire_code() == CODE_SECRET:
                    passer_en_desarmee()

            elif etat_actuel == "Déclenchée":
                print("→ Saisir code pour DÉSARMER :")
                if lire_code() == CODE_SECRET:
                    passer_en_desarmee()

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[INFO] Arrêt demandé par l'utilisateur")
    finally:
        stop_pir.set()
        _stop_buzzer.set()
        led(False, False, False)
        GPIO.cleanup()
        print("[INFO] GPIO libérés. Fin du programme.")

