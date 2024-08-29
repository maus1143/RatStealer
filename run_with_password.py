from cryptography.fernet import Fernet
import subprocess
import getpass
import os

def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

def load_encrypted_password():
    with open("encrypted_password.bin", "rb") as password_file:
        return password_file.read()

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

def check_password(input_password, encrypted_password, key):
    decrypted_password = decrypt_password(encrypted_password, key)
    return input_password == decrypted_password

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

key = load_key()
encrypted_password = load_encrypted_password()

input_password = getpass.getpass("Bitte geben Sie das Passwort ein: ")

if check_password(input_password, encrypted_password, key):
    print("Passwort korrekt. Das Skript wird ausgeführt.")
    clear_screen()
    subprocess.run(["python", "send.py"]) 
else:
    print("Passwort inkorrekt. Zugriff verweigert.")
