import sqlite3
from account import Account
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

if __name__ == "__main__":
    try:
        db_conn = sqlite3.connect('finance-tracker.sqlite')
        c = db_conn.cursor()
        c.execute('''CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, salt TEXT, password TEXT)''')
        c.execute(
            '''CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT, username TEXT, website TEXT, password TEXT, FOREIGN KEY(owner) REFERENCES accounts(username))''')
        db_conn.commit()
        db_conn.close()
        print("ok")
    except:
        print("ok")