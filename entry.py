import sqlite3
from account import Account


class Entry:
    def __init__(self, user: Account, username, website, password):
        self.owner = user
        self.username = username
        self.website = website
        self.password = password

    def add(self, user: Account, website: str, plain_password: str):
        # add new entry for given user object
        try:
            db_conn = sqlite3.connect('password-manager.sqlite')
            c = db_conn.cursor()
            db_query = c.execute(
                '''INSERT INTO `entries` ('owner','username','salt','password') VALUES ("{self.owner.username}", "{self.username}", "{self.website}", "{self.password}")''')
            db_query.execute()
            db_conn.close()
            return True
        except:
            return False

    def __str__(self):
        return f"{self.website} {self.username}"
