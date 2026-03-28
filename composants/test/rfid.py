from mfrc522 import SimpleMFRC522 as RFIDReader

reader = RFIDReader()

print("En attente...")

try:
    while True:
        badgeId, text = reader.read()
        print("ID :", badgeId)
        print("Texte :", text)
        print("-----")

except KeyboardInterrupt:
    print("Stop")