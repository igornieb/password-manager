import sqlite3
from account import Account
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


class Entry:
    def __init__(self, user: Account, username, website, password):
        self.owner = user
        self.username = username
        self.website = website
        self.password = password

    def add(self):
        if self.owner.is_authenticated():
            hashed_password = self.encrypt()
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(f'''INSERT INTO `entries` ('owner','username','website','password') VALUES ("{self.owner.username}", "{self.username}", "{self.website}", "{hashed_password}")''')
            db_conn.commit()
            db_conn.close()
            return True
        return False

    def encrypt(self):
        if self.owner.is_authenticated():
            message = self.password
            key = PBKDF2(str(self.owner.hashed_password), self.owner.salt).read(32)
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
            key = PBKDF2(str(self.owner.hashed_password), self.owner.salt).read(32)
            nonce = convert[-16:]
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(convert[:-16])
            return plaintext.decode()
        else:
            return ""

    # def __str__(self):
    #     return f"{self.username} {self.website} {self.password}"

    def __repr__(self):
        if self.owner.is_authenticated():
            return f"{self.username} {self.website} {self.decrypt()}"
        return f"{self.username} {self.website}"
