from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if not os.path.exists("avatar.db"):
        with sqlite3.connect("avatar.db") as conn:
            conn.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    q1 TEXT,
                    q2 TEXT,
                    q3 TEXT,
                    q4 TEXT,
                    q5 TEXT,
                    avatar TEXT
                )
            ''')

def assign_avatar(q1, q2, q3, q4, q5):
    if q1 == "Korra" or q3 == "Polar Bear Dog" or (q2 == "A spicy dish" and q5 == "Openly and passionately"):
        return "Korra (Water Tribe)"
    elif q1 == "Aang" or q3 == "Flying Bison" or (q4 == "Evade" and q5 == "Calmly and introspectively"):
        return "Aang (Air Nomad)"
    elif q1 == "Kyoshi" or q3 == "Badgermole" or (q2 == "A hearty banquet" and q4 == "Stand your ground"):
        return "Toph (Earth Kingdom)"
    elif q1 == "Roku" or q3 == "Dragon" or (q2 == "A seafood feast" and q4 == "Counterstrike"):
        return "Zuko (Fire Nation)"
    else:
        return "Unknown Element"

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/quiz", methods=["POST"])
def quiz():
    username = request.form["username"]
    return render_template("form.html", username=username)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    q1 = request.form["q1"]
    q2 = request.form["q2"]
    q3 = request.form["q3"]
    q4 = request.form["q4"]
    q5 = request.form["q5"]

    avatar = assign_avatar(q1, q2, q3, q4, q5)

    with sqlite3.connect("avatar.db") as conn:
        conn.execute("""
            INSERT INTO users (username, q1, q2, q3, q4, q5, avatar)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, q1, q2, q3, q4, q5, avatar))

    return render_template("result.html", username=username, avatar=avatar)

@app.route("/results")
def results():
    with sqlite3.connect("avatar.db") as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
    return render_template("results.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))


