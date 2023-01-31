import string
import secrets
import sqlite3
from account import Account
from entry import Entry

def pswd_gen(length: int):
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters+digits+special_chars
    pwd = ''
    for i in range(length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd

def search_db(user: Account, query: str):
    results = []
    if user.is_authenticated():
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_query = c.execute(
            f'''SELECT id, username, website, password FROM entries WHERE owner="{user.username}" AND username LIKE "%{query}%" OR website like "%{query}%"''')
        for res in db_query:
            results.append(Entry(res[0], user, res[1], res[2], res[3]))
        db_conn.close()
    return results


def all_entries(user: Account):
    results = []
    if user.is_authenticated():
        db_conn = sqlite3.connect('password-manager.sqlite')
        c = db_conn.cursor()
        db_query = c.execute(
            f'''SELECT id, username, website, password FROM entries WHERE owner="{user.username}"''')
        for res in db_query:
            results.append(Entry(res[0], user, res[1], res[2], res[3]))
        db_conn.close()
    return results

if __name__=="__main__":
    print(pswd_gen(20))
