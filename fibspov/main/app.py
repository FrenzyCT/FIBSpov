from flask import Flask, render_template, jsonify, request, flash, redirect, session
from fibspov.main.database import get_db, create_user
import os

app = Flask(__name__)

#created secret key and delete print after generated key
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/register', methods=['GET'])
def register_page():
    return render_template(
        "register.html"
    )
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get("name")

    if not name:
        flash("Ikke gyldig navn eller passord FIBS kriger")
        return redirect("/register")
    #check for existing user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
    existing = cursor.fetchone()
    cursor.close()
    conn.close()

    if existing:
        flash("Brukeren er allerede logget inn")
        return redirect("/register")
    #make a user
    create_user(name)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
    user_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    session["user"] = name
    session["user_id"] = user_id

    flash("Brukeren er opprettet")
    return redirect("/")


@app.route('/')
def index():
    if "user" not in session:
        return redirect("/register")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM counts WHERE user_id = %s", (session["user_id"],))
    rows = cursor.fetchall()
    counts = {row[0]: row[1] for row in rows}

    cursor.close()
    conn.close()

    return render_template("index.html", counts=counts)

@app.route('/count/<counter>', methods=['POST'])
def count(counter):
    conn = get_db()
    cursor = conn.cursor()
    #if rows do not exist, insert it
    cursor.execute("""
        INSERT INTO counts (name, value, user_id) VALUES (%s, 0, %s)
        ON CONFLICT DO NOTHING
        """, (counter, session["user_id"]))

    #updates value
    cursor.execute("""UPDATE counts SET value = value + 1 WHERE name = %s AND user_id = %s
                   """, (counter, session["user_id"]))
    conn.commit()

    cursor.execute("""SELECT value FROM counts WHERE name = %s AND user_id = %s
                   """, (counter, session["user_id"]))
    # PostgreSQL returns a tuple, not dicts
    value = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({"name": counter, "value": value})

@app.route("/reset", methods=['POST'])
def reset():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""UPDATE counts SET value=0 WHERE user_id = %s""", (session["user_id"],))

    conn.commit()

    cursor.execute("""SELECT name, value FROM counts WHERE user_id = %s
                   """, (session["user_id"],))
    rows = cursor.fetchall()
    counts = {row[0]: row[1] for row in rows}

    cursor.close()
    conn.close()

    return jsonify(counts)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")
