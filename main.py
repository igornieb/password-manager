import sqlite3
from account import Account
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from base64 import b64encode, b64decode


# TODO tkinker gui
# TODO decrypt/encrypt
# TODO copy to clipboard on click
# TODO store salt and pepper

def search_db(user: Account, query: str):
    if user.is_authenticated():
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_query = c.execute(
            f'''SELECT username, website, password FROM entries WHERE owner="{user.username}" AND username LIKE "%{query}%" OR website like "%{query}%"''')
        db_conn.close()
        return list(db_query)
    else:
        return list()


if __name__ == "__main__":
    try:
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        c.execute(
            '''CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, salt TEXT, password TEXT)''')
        c.execute(
            '''CREATE TABLE entries (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT, username TEXT, website TEXT, password TEXT, FOREIGN KEY(owner) REFERENCES accounts(username))''')
        db_conn.commit()
        db_conn.close()
        print("ok")
    except:
        print("ok")
