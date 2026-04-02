import RPi.GPIO as GPIO
import time
import threading

# ── Numérotation BCM ────────────────────────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ── Broches ─────────────────────────────────────────────────────────────────
PIN_LED_R  = 17
PIN_LED_G  = 27
PIN_LED_B  = 22
PIN_PIR    = 15
PIN_BUZZER = 18

# Keypad 4x4 — 4 lignes (sorties) + 4 colonnes (entrées pull-up)
ROWS = [5, 6, 13, 19]        # R1 R2 R3 R4
COLS = [26, 12, 16, 20]      # C1 C2 C3 C4

KEYPAD_MAP = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D'],
]

# ── Code secret (modifiable ici) ─────────────────────────────────────────────
CODE_SECRET = "1234"

# ── Configuration GPIO ───────────────────────────────────────────────────────
GPIO.setup(PIN_LED_R,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_G,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_LED_B,  GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN_PIR,    GPIO.IN)

for row in ROWS:
    GPIO.setup(row, GPIO.OUT, initial=GPIO.HIGH)
for col in COLS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ── État global ──────────────────────────────────────────────────────────────
etat = "desarmee"
etat_lock = threading.Lock()

_stop_buzzer   = threading.Event()
_thread_buzzer = None


# ════════════════════════════════════════════════════════════════════════════
# LED RGB
# ════════════════════════════════════════════════════════════════════════════

def led(r=False, g=False, b=False):
    """Allume la LED RGB avec la couleur voulue."""
    GPIO.output(PIN_LED_R, GPIO.HIGH if r else GPIO.LOW)
    GPIO.output(PIN_LED_G, GPIO.HIGH if g else GPIO.LOW)
    GPIO.output(PIN_LED_B, GPIO.HIGH if b else GPIO.LOW)

def led_bleu():  led(b=True)
def led_vert():  led(g=True)
def led_rouge(): led(r=True)
def led_off():   led()


# ════════════════════════════════════════════════════════════════════════════
# Buzzer
# ════════════════════════════════════════════════════════════════════════════

def bip(nb=1, duree=0.08, pause=0.12):
    """Émet nb bip(s) courts."""
    for _ in range(nb):
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(duree)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(pause)

def _buzzer_continu(stop_event: threading.Event):
    """Boucle interne : buzzer ON/OFF jusqu'à stop_event."""
    while not stop_event.is_set():
        GPIO.output(PIN_BUZZER, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(PIN_BUZZER, GPIO.LOW)


# ════════════════════════════════════════════════════════════════════════════
# Keypad 4x4
# ════════════════════════════════════════════════════════════════════════════

def lire_touche():
    """
    Scan matriciel : met chaque ligne à LOW tour à tour
    et lit les colonnes. Retourne la touche ou None.
    """
    for i, row in enumerate(ROWS):
        GPIO.output(row, GPIO.LOW)
        for j, col in enumerate(COLS):
            if GPIO.input(col) == GPIO.LOW:
                time.sleep(0.05)                   # anti-rebond
                while GPIO.input(col) == GPIO.LOW:
                    pass                            # attente relâchement
                GPIO.output(row, GPIO.HIGH)
                return KEYPAD_MAP[i][j]
        GPIO.output(row, GPIO.HIGH)
    return None

def lire_code(nb_chiffres=4, timeout=30):
    """
    Attend nb_chiffres touches numériques sur le keypad.
    Retourne la chaîne saisie ou '' si timeout.
    """
    saisi = ""
    debut  = time.time()
    print("  Code : ", end="", flush=True)
    while len(saisi) < nb_chiffres:
        if time.time() - debut > timeout:
            print("\n  [Timeout — saisie annulée]")
            return ""
        touche = lire_touche()
        if touche and touche.isdigit():
            saisi += touche
            print("*", end="", flush=True)
        time.sleep(0.05)
    print()
    return saisi


# ════════════════════════════════════════════════════════════════════════════
# Transitions d'état
# ════════════════════════════════════════════════════════════════════════════

def passer_en_desarmee():
    global etat, _thread_buzzer
    _stop_buzzer.set()
    if _thread_buzzer and _thread_buzzer.is_alive():
        _thread_buzzer.join()
    with etat_lock:
        etat = "desarmee"
    led_bleu()
    print("[ÉTAT] ● DÉSARMÉE — LED bleue")

def passer_en_armee():
    global etat
    with etat_lock:
        etat = "armee"
    led_vert()
    bip(nb=2)                           # 2 petits bips = armée avec succès
    print("[ÉTAT] ● ARMÉE — LED verte — PIR actif")

def passer_en_declenchee():
    global etat, _thread_buzzer
    with etat_lock:
        etat = "declenchee"
    led_rouge()
    print("[ÉTAT] ● DÉCLENCHÉE — LED rouge — buzzer actif")
    _stop_buzzer.clear()
    _thread_buzzer = threading.Thread(
        target=_buzzer_continu, args=(_stop_buzzer,), daemon=True
    )
    _thread_buzzer.start()


# ════════════════════════════════════════════════════════════════════════════
# Thread : surveillance PIR
# ════════════════════════════════════════════════════════════════════════════

def _surveiller_pir(stop_evt: threading.Event):
    """Lit le PIR toutes les 100 ms. Déclenche si mouvement et armée."""
    print("[PIR] Surveillance démarrée")
    while not stop_evt.is_set():
        with etat_lock:
            etat_local = etat
        if etat_local == "armee" and GPIO.input(PIN_PIR) == GPIO.HIGH:
            print("[PIR] ⚠ Mouvement détecté !")
            passer_en_declenchee()
        time.sleep(0.1)


# ════════════════════════════════════════════════════════════════════════════
# Boucle principale
# ════════════════════════════════════════════════════════════════════════════

def boucle_principale():
    global etat

    # Démarrage : LED bleue (désarmée)
    passer_en_desarmee()

    # Thread PIR en arrière-plan
    stop_pir   = threading.Event()
    thread_pir = threading.Thread(
        target=_surveiller_pir, args=(stop_pir,), daemon=True
    )
    thread_pir.start()

    print("\n=== Système d'alarme démarré ===")
    print("  Tapez le code sur le keypad pour armer / désarmer.\n")

    try:
        while True:
            with etat_lock:
                etat_local = etat

            # ── DÉSARMÉE : attente d'un code pour armer ──────────────────────
            if etat_local == "desarmee":
                print("  → Saisir le code pour ARMER :")
                code = lire_code(nb_chiffres=len(CODE_SECRET))
                if code == CODE_SECRET:
                    print("  ✔ Code correct → armement")
                    passer_en_armee()
                elif code != "":
                    print("  ✘ Code incorrect")
                    bip(nb=1, duree=0.4)           # 1 bip long = erreur

            # ── ARMÉE : le thread PIR gère le déclenchement ──────────────────
            elif etat_local == "armee":
                time.sleep(0.1)

            # ── DÉCLENCHÉE : attente du code pour désarmer ───────────────────
            elif etat_local == "declenchee":
                print("  → Saisir le code pour DÉSARMER :")
                code = lire_code(nb_chiffres=len(CODE_SECRET))
                if code == CODE_SECRET:
                    print("  ✔ Code correct → désarmement")
                    passer_en_desarmee()
                elif code != "":
                    print("  ✘ Code incorrect — alarme maintenue")

    except KeyboardInterrupt:
        print("\n[INFO] Arrêt demandé (Ctrl+C)")

    finally:
        stop_pir.set()
        _stop_buzzer.set()
        led_off()
        GPIO.cleanup()
        print("[INFO] GPIO libérés. Fin du programme.")

