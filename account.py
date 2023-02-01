import hashlib
import sqlite3
import secrets
import string


class Account:
    login_salt = "salt for logging in"

    def __init__(self, username="", password=""):
        self.authenticated = False
        self.username = username
        self.salt = ""
        self.hashed_password = hashlib.sha256((password + self.login_salt).encode()).hexdigest()

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
            if db_password == self.hashed_password:
                self.salt = c.execute(f"SELECT salt FROM `accounts` WHERE username='{self.username}'").fetchone()[0]
                self.authenticated = True
                db_conn.close()
                return True
            else:
                db_conn.close()
                return False
        except:
            return False

    def register(self):
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            alphabet = string.ascii_letters + string.digits
            self.salt = ''.join(secrets.choice(alphabet) for i in range(100))
            c.execute(
                f'''INSERT INTO `accounts`('username','salt','password') VALUES ("{self.username}", "{self.salt}", "{self.hashed_password}")''')
            db_conn.commit()
            db_conn.close()
            return True
        except:
            return False

    # TODO change_password, delete_account

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

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"{self.username}"
