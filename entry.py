import secrets
import sqlite3
import string
from account import Account
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class Entry:
    def __init__(self, index, user: Account, username, website, password):
        self.id = index
        self.owner = user
        self.salt = self.get_salt_for_entry()
        self.username = username
        self.website = website
        self.password = password

    def add(self):
        if self.owner.is_authenticated():
            hashed_password = self.encrypt()
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(
                f'''INSERT INTO `entries` ('owner','username','website','password','salt') VALUES ("{self.owner.username}", "{self.username}", "{self.website}", "{hashed_password}", "{self.salt}")''')
            db_conn.commit()
            db_conn.close()
            return True
        return False

    def delete(self):
        if self.owner.is_authenticated():
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(f'''DELETE FROM `entries` WHERE id="{self.id}" AND owner="{self.owner.username}"''')
            db_conn.commit()
            db_conn.close()
            return True
        return False

    def update(self, new_username, new_website, new_password):
        if self.owner.is_authenticated():
            self.password = new_password
            hashed_password = self.encrypt()
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(
                f'''UPDATE entries SET username = "{new_username}" , website = "{new_website}", password="{hashed_password}" Where id="{self.id}" AND owner="{self.owner}"''')
            db_conn.commit()
            db_conn.close()
            self.username = new_username
            self.website = new_website
            self.password = hashed_password
            return True
        return False

    def encrypt(self):
        if self.owner.is_authenticated():
            message = self.password
            key = PBKDF2(str(self.salt), self.owner.salt).read(32)
            data_convert = str.encode(message)
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data_convert)
            add_nonce = ciphertext + nonce
            encoded_ciphertext = b64encode(add_nonce).decode()
            return encoded_ciphertext
        return ""

    def decrypt(self):
        if self.owner.is_authenticated():
            message = self.password
            if len(message) % 4:
                message += '=' * (4 - len(message) % 4)
            convert = b64decode(message)
            key = PBKDF2(str(self.salt), str(self.owner.salt)).read(32)
            nonce = convert[-16:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(convert[:-16])
            return plaintext.decode()
        else:
            return ""

    def get_salt_for_entry(self):
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(f'''SELECT salt FROM entries Where id="{self.id}" AND owner="{self.owner}"''')
            salt = db_query.fetchone()[0]
            db_conn.close()
            return salt
        except:
            alphabet = string.ascii_letters + string.digits
            return ''.join(secrets.choice(alphabet) for i in range(100))

    # def __str__(self):
    #     return f"{self.username} {self.website} {self.password}"

    def __repr__(self):
        if self.owner.is_authenticated():
            return f"{self.username} {self.website} {self.password}"
        return f"{self.username} {self.website}"
