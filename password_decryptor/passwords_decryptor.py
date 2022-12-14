# Full Credits to LimerBoy
import os
import re
import sys
import json
import base64
import sqlite3

import pywintypes
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import csv


# GLOBAL CONSTANT
# CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
# CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))
# GLOBAL CONSTANT
# CHROME_PATH_LOCAL_STATE = r"C:\Users\Stefan\PycharmProjects\accounts_manager\profiles\v2 - 100\Local State"
# CHROME_PATH = r"C:\Users\Stefan\PycharmProjects\accounts_manager\profiles\v2 - 100"
def get_secret_key_from_file(path):
    with open(fr'{path}\secret', "rb") as secret_file:
        secret_key = secret_file.read()
        secret_key = win32crypt.CryptProtectData(secret_key)
        secret_key = (base64.b64encode(b"DPAPI" + secret_key)).decode("utf-8")
        return secret_key


def write_secret_key_to_file(path, secret_key):
    CHROME_PATH_LOCAL_STATE = fr'{path}\Local State'
    with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
        testt = local_state["os_crypt"]["encrypted_key"]
        print(testt)
        local_state["os_crypt"]["encrypted_key"] = secret_key

    with open(CHROME_PATH_LOCAL_STATE, "w", encoding='utf-8') as f:
        json.dump(local_state, f)


def encrypt_secret_key(secret_key):
    encrypted_secret_key = win32crypt.CryptProtectData(secret_key)
    return encrypted_secret_key


def get_secret_key(path):
    CHROME_PATH_LOCAL_STATE = fr'{path}\Local State'

    try:
        # (1) Get secretkey from chrome local state
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        print(f'secret_key: {secret_key}')
        # Remove suffix DPAPI
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key)[1]
        return secret_key
    except pywintypes.error as e:
        if e.funcname == "CryptUnprotectData":
            return 'error'
    # except Exception as e:
    #     print("%s" % str(e))
    #     print(type(e))
    #     # if 'CryptUnprotectData' in e:
    #     #     print("A"*1000)
    #     print("[ERR] Chrome secretkey cannot be found")
    #     return None


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(ciphertext, secret_key):
    try:
        # (3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        # (3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        # Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        # (4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""


def get_db_connection(chrome_path_login_db):
    try:
        print(chrome_path_login_db)
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        print("%s" % str(e))
        print("[ERR] Chrome database cannot be found")
        return None


def do_decrypt(path):
    CHROME_PATH = path
    passwords = ''
    try:
        # Create Dataframe to store passwords
        secret_key = get_secret_key(path)
        if secret_key == 'error':
            print(path)
            key = get_secret_key_from_file(path)
            write_secret_key_to_file(path, key)
            secret_key = get_secret_key(path)

        with open(fr'{path}\secret', "wb") as secret_file:
            if secret_key != "":
                secret_file.write(secret_key)
            else:
                raise BaseException("empty secret_key")
        with open(fr'{path}\decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index", "url", "username", "password"])
            # (1) Get secret key

            print(f"secret key: {secret_key}")
            # Search user profile or default folder (this is where the encrypted login password is stored)
            folders = [element for element in os.listdir(CHROME_PATH) if
                       re.search("^Profile*|^Default$", element) != None]
            for folder in folders:
                # (2) Get ciphertext from sqlite database
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
                conn = get_db_connection(chrome_path_login_db)
                if (secret_key and conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for index, login in enumerate(cursor.fetchall()):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if (url != "" and username != "" and ciphertext != ""):
                            # (3) Filter the initialisation vector & encrypted password from ciphertext
                            # (4) Use AES algorithm to decrypt the password
                            decrypted_password = decrypt_password(ciphertext, secret_key)
                            passwords += f'Sequence: {index}\nURL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n{"*" * 50}\n'
                            # print("Sequence: %d" % (index))
                            # print("URL: %s\nUser Name: %s\nPassword: %s\n" % (url, username, decrypted_password))
                            # print("*" * 50)
                            # (5) Save into CSV
                            csv_writer.writerow([index, url, username, decrypted_password])
                    # Close database connection
                    cursor.close()
                    conn.close()
                    # Delete temp login db
                    os.remove("Loginvault.db")
                    return passwords
    except Exception as e:
        print("[ERR] " % str(e))


if __name__ == '__main__':
    # print(get_secret_key(r"C:\Users\Stefan\PycharmProjects\accounts_manager\profiles\test"))
    print(do_decrypt(r"C:\Users\Stefan\PycharmProjects\accounts_manager\profiles\v2 - 146"))
    # key = get_secret_key_from_file(r"C:\Users\Stefan\PycharmProjects\accounts_manager\profiles\test1")
    # print(base64.b64encode(encrypt_secret_key(key)))
    # print(encrypt_secret_key(key).decode("utf-8"))
    # encrypt_secret_key(b"\x86*\xcfz`=gr\xca\x89^\x19)\xa7\x15\xfd\xb5\x1ae\xf8\xac\xdd\xdd\xc1\x04_\xbf6\x95")
    # print(do_decrypt(r"C:\Users\Stefan\AppData\Local\Google\Chrome\User Data"))
