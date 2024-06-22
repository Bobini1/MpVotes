from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_mps():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT id, name from mp")
    mps = cur.fetchall()
    mp_dicts = []
    for mp in mps:
        mp_dicts.append({"id": mp[0], "name": mp[1]})
    cur.close()
    con.close()
    return mp_dicts


mps = get_mps()


@app.route('/')
def home():
    return render_template('index.html', mps=mps)


@app.route('/mps/<mp_id>')
def mp_page(mp_id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute("SELECT voting.title, voting.topic, vote.vote FROM mp JOIN vote ON vote.mp_id == ? JOIN voting ON vote.voting_id = voting.id", (mp_id,))
    votes = cur.fetchall()
    cur.execute("SELECT name FROM mp WHERE id == ?", (mp_id,))
    name, = cur.fetchone()
    cur.close()
    con.close()
    votes_dicts = []
    for vote in votes:
        title = vote[0]
        if vote[1]:
            title += " - " + vote[1]
        votes_dicts.append({"title": title, "vote": vote[2]})
    return render_template('mp.html', votes=votes_dicts, name=name)


if __name__ == '__main__':
    app.run()
