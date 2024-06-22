import sqlite3
import json
import requests

con = sqlite3.connect("db.db")
url = "https://api.sejm.gov.pl/sejm"


def create_db():
    db = con.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS scans(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS mp(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING UNIQUE)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS voting(id INTEGER PRIMARY KEY AUTOINCREMENT, title STRING, topic STRING, description "
        "STRING)")
    db.execute(
        "CREATE TABLE IF NOT EXISTS vote(id INTEGER PRIMARY KEY AUTOINCREMENT, mp_id INTEGER, voting_id INTEGER, "
        "vote STRING)")
    con.commit()


if __name__ == '__main__':
    create_db()
