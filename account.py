import hashlib
import sqlite3
import secrets
import string


class Account:
    def __init__(self, username="", password=""):
        self.authenticated = False
        self.username = username
        self.salt = self.get_salt_for_username()
        self.hashed_password = hashlib.sha256((password + self.salt).encode()).hexdigest()

    def is_authenticated(self):
        if self.authenticated==True:
            return True
        return False

    def login(self):
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_password = c.execute(f"SELECT password FROM `accounts` WHERE username='{self.username}'")
            db_password = db_password.fetchone()[0]
            db_conn.close()
            if db_password == self.hashed_password:
                self.authenticated = True
                return True
            else:
                return False
        except:
            return False

    def register(self):
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            c.execute(
                f'''INSERT INTO `accounts`('username','salt','password') VALUES ("{self.username}", "{self.salt}", "{self.hashed_password}")''')
            db_conn.commit()
            db_conn.close()
            return True
        except:
            return False

    # TODO change_password

    def delete(self):
        if self.is_authenticated():
            try:
                db_conn = sqlite3.connect('password-manager.sqlite')
                c = db_conn.cursor()
                c.execute(f"DELETE FROM `accounts` WHERE username='{self.username}'")
                db_conn.commit()
                db_conn.close()
            except:
                return "err"

    def get_salt_for_username(self):
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(f'''SELECT salt FROM accounts WHERE username="{self.username}"''')
            salt = db_query.fetchone()[0]
            db_conn.close()
            return salt
        except:
            alphabet = string.ascii_letters + string.digits
            return ''.join(secrets.choice(alphabet) for i in range(100))

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"{self.username}"
