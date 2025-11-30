from flask import Flask, render_template, request
import sqlite3
import os

from odibat import *
from odibowl import *
from t20bat import *
from t20bowl import *
from testbat import *
from testbowl import *

# -----------------------------------------
# Flask App (static folder fixed)
# -----------------------------------------
app = Flask(__name__, static_url_path="/static", static_folder="static")

# -----------------------------------------
# Correct database path
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "user_data.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
            name TEXT,
            password TEXT,
            mobile TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()


# -----------------------------------------
# ROUTES
# -----------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("userlog.html")


@app.route("/userlog", methods=["GET", "POST"])
def userlog():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # SAFE SQL (no injection)
        cursor.execute("SELECT * FROM user WHERE name=? AND password=?", (name, password))
        result = cursor.fetchall()
        conn.close()

        if len(result) == 0:
            return render_template("index.html", msg="Incorrect Credentials. Try Again.")
        else:
            return render_template("userlog.html")

    return render_template("index.html")


@app.route("/userreg", methods=["POST"])
def userreg():
    name = request.form["name"]
    password = request.form["password"]
    mobile = request.form["phone"]
    email = request.form["email"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # SAFE SQL
    cursor.execute("INSERT INTO user (name, password, mobile, email) VALUES (?, ?, ?, ?)",
                   (name, password, mobile, email))
    conn.commit()
    conn.close()

    return render_template("index.html", msg="Successfully Registered!")


@app.route("/predict", methods=["POST"])
def predict():
    mode = request.form["mode"]
    bat = int(request.form["bat"])
    bowl = int(request.form["bowl"])
    name = request.form["name"]
    oname = request.form["oname"]

    total = bat + bowl
    if total != 11:
        return render_template("userlog.html", msg="Error: Batsmen + Bowlers must equal 11")

    try:
        if mode == "ODI":
            bt = custom_ODI_bats(bat, name, oname)
            bl = custom_ODI_bowl(bowl, name, oname)

        elif mode == "T20":
            bt = custom_T20_bats(bat, name, oname)
            bl = custom_T20_bowl(bowl, name, oname)

        elif mode == "TEST":
            bt = custom_test_bats(bat, name, oname)
            bl = custom_test_bowl(bowl, name, oname)  # FIXED (was ODI)

        # Prepare lists for HTML
        bts = [[row["Player"], row["Mat"], row["Ave"], row["Runs"]] for _, row in bt.iterrows()]
        bls = [[row["Player"], row["Mat"], row["Mdns"], row["Ave"], row["Econ"]] for _, row in bl.iterrows()]

        return render_template("userlog.html", bts=bts, bls=bls)

    except Exception as e:
        return render_template("userlog.html", msg=f"Error: {str(e)}")


@app.route("/logout")
def logout():
    return render_template("index.html")


# -----------------------------------------
# RUN
# -----------------------------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
