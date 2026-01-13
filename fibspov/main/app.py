from flask import Flask, render_template, jsonify
from fibspov.main.database import get_db


app = Flask(__name__)

#can be removed, replaced by database:
'''counts = { 
    "phone": 0,
    "direct": 0
}'''
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM counts")
    rows = cursor.fetchall()
    counts = {row["name"]: row["value"] for row in rows}
    return render_template("index.html", counts=counts)

@app.route('/count/<counter>', methods=['POST'])
def count(counter):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE counts SET value = value + 1 WHERE name = ?", (counter,))
    conn.commit()

    cursor.execute("SELECT value FROM counts WHERE name = ?", (counter,))
    value = cursor.fetchone()["value"]

    return jsonify({"name": counter, "value": value})

@app.route("/reset", methods=['POST'])
def reset():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE counts SET value=0 WHERE name IN ('phone', 'direct')")
    conn.commit()

    cursor.execute("SELECT name, value FROM counts")
    rows = cursor.fetchall()
    counts = {row["name"]: row["value"] for row in rows}
    return jsonify(counts)


