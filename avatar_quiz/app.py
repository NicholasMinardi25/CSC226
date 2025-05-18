
import os
import psycopg2
from flask import Flask, render_template, request
from collections import defaultdict

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")

def init_db():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as c:
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT,
                    q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT,
                    q5 TEXT, q6 TEXT, q7 TEXT, q8 TEXT,
                    element TEXT
                )
            ''')
            conn.commit()

@app.route("/")
def homepage():
    return render_template("Avatar.html")

@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/characters")
def characters():
    return render_template("characters.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/quiz", methods=["POST"])
def quiz():
    username = request.form.get("username")
    return render_template("form.html", username=username)

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    answers = [request.form.get(f"q{i}") for i in range(1, 9)]
    element_scores = {"Water": 0, "Earth": 0, "Fire": 0, "Air": 0}

    for answer in answers:
        answer = answer.lower()
        if any(word in answer for word in ["aang", "seafood", "flying bison", "evade", "freedom", "sky", "spring", "adapt"]):
            element_scores["Air"] += 1
        if any(word in answer for word in ["roku", "banquet", "badgermole", "stand", "justice", "mountains", "fall", "stability"]):
            element_scores["Earth"] += 1
        if any(word in answer for word in ["korra", "spicy", "dragon", "offense", "victory", "city", "summer", "passion"]):
            element_scores["Fire"] += 1
        if any(word in answer for word in ["kyoshi", "vegetarian", "polar bear", "counterstrike", "balance", "ocean", "winter", "community"]):
            element_scores["Water"] += 1

    element = max(element_scores, key=element_scores.get)

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as c:
            c.execute('''
                INSERT INTO users (username, q1, q2, q3, q4, q5, q6, q7, q8, element)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (username, *answers, element))
            conn.commit()

    return render_template("result.html", username=username, element=element)

@app.route("/results")
def results():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as c:
            c.execute("SELECT username, element FROM users")
            data = c.fetchall()

    grouped = defaultdict(list)
    for username, element in data:
        grouped[element].append(username)

    labels = list(grouped.keys())
    counts = [len(grouped[e]) for e in labels]

    return render_template("results.html", grouped=grouped, labels=labels, data=counts)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
