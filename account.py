import hashlib
import sqlite3
import secrets


class Account:
    login_salt = "salt for logging in"

    def __init__(self, username, password):
        self.username = username
        self.salt = ""
        self.hashed_password = hashlib.sha256((password + self.login_salt).encode()).hexdigest()

    def login(self):
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_pass = c.execute(f"SELECT 'password' FROM `accounts` WHERE username='{self.username}'")
        db_conn.close()
        if db_pass == self.hashed_password:
            self.salt = c.execute(f"SELECT 'salt' FROM `accounts` WHERE username='{self.username}'")
            return True
        else:
            return False

    def register(self):
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_username = c.execute(f"SELECT 'username' FROM `accounts` WHERE username='{self.username}'")
        if db_username != self.username:
            self.salt = str(secrets.SystemRandom())
            c.execute(
                f'''INSERT INTO `accounts`('username','salt','password') VALUES ("{self.username}", "{self.salt}", "{self.hashed_password}")''')
            db_conn.commit()
            db_conn.close()
            return True
        else:
            return False

    # TODO change_password, delete_account
    def __str__(self):
        return self.username
