import sqlite3
import json
import requests

con = sqlite3.connect("db.db")
url = "https://api.sejm.gov.pl/sejm"


def populate_db():
    db = con.cursor()
    # db.execute("SELECT timestamp FROM scans")
    # timestamp = db.fetchone()
    # timestamp = datetime.fromtimestamp(timestamp or 0)
    terms_path = url + "/term"
    terms_json = requests.get(terms_path)
    term_arr = json.loads(terms_json.text)
    current_term = term_arr[-1]
    proceedings_path = terms_path + str(current_term["num"]) + "/proceedings"
    proceedings_arr = json.loads(requests.get(proceedings_path).text)
    votings = []
    for proceeding in proceedings_arr:
        number = proceeding["number"]
        path = terms_path + str(current_term["num"]) + "/votings/" + str(number)
        votings_this_proceeding = json.loads(requests.get(path).text)
        for voting in votings_this_proceeding:
            votings.append({"number": number, "voting": voting})
    for voting in votings:
        details_path = terms_path + str(current_term["num"]) + "/votings/" + str(voting["number"]) + "/" + str(
            voting["voting"]["votingNumber"])
        details = json.loads(requests.get(details_path).text)
        db.execute("INSERT INTO voting(title, topic, description) VALUES(?, ?, ?)",
                   (details["title"], details.get("topic", None), details.get("description", None)))
        voting_id = db.lastrowid
        for vote in details["votes"]:
            name = f"{vote["firstName"]} {vote["lastName"]}"
            db.execute("INSERT OR IGNORE INTO mp(name) VALUES(?)", (name,))
            con.commit()
            db.execute("SELECT id FROM mp WHERE name == ?", (name,))
            mp_id, = db.fetchone()
            vote_str = vote["vote"]
            if "votingOptions" in details:
                vote_str = None
                for option in details["votingOptions"]:
                    if vote["listVotes"].get(str(option["optionIndex"]), "NO") == "YES":
                        vote_str = option["option"]

            db.execute("INSERT INTO vote(mp_id, voting_id, vote) VALUES(?, ?, ?)", (mp_id, voting_id, vote_str))
    print("done")


if __name__ == '__main__':
    populate_db()
