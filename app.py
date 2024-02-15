import sys

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///players.db")

@app.route("/", methods=["GET", "POST"])
def home():
    # Find and show active players on table
    gamers = db.execute("SELECT userid, username FROM users")
    return render_template("home.html", gamers=gamers)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Add user to database
        try:
            id = db.execute("INSERT INTO users (username, password) VALUES(?, ?)",
                            request.form.get("username"),
                            generate_password_hash(request.form.get("password")))
            rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
            db.execute("INSERT INTO traits (user_id) VALUES(?)", rows[0]["userid"])
        except ValueError:
            return redirect("register.html")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/death")

    # GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return redirect("/")

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]

        # Redirect user to home page
        return redirect("/death")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/death")
@login_required
def death():
    return render_template("death.html")


@app.route("/trolley", methods=["GET", "POST"])
@login_required
def trolley():

    if request.method == "POST":
        data = request.get_json()
        for key in data:
            db.execute("UPDATE traits SET ? = ? WHERE user_id = ?", key, data[key], session["user_id"])
        return redirect("torture")

    else:
        return render_template("trolley.html")


@app.route("/torture", methods=["GET", "POST"])
@login_required
def torture():
    traits = db.execute("SELECT * FROM traits WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        data = request.get_json()
        for key in data:
            db.execute("UPDATE traits SET ? = ? WHERE user_id = ?", key, data[0][key], session["user_id"])
        return redirect("torture")

    return render_template("torture.html", traits=traits)

@app.route("/questions")
@login_required
def questions():
    return render_template("questions.html")