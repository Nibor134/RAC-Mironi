import sqlite3
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, send_file

from lib.functions import *

# Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

Authed = False

#Main Route
@app.route("/")
def redirectpage():
    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    global Authed
    if request.method == "POST":
        if request.form.get('LoginButton'):
            if login_check():
                Authed = True
        elif request.form.get('SignupPageButton'):
            return redirect(url_for("signup"))
        elif request.form.get('HomeButton'):
            return redirect(url_for("login"))

    if Authed == False:
        return render_template("login.html")
    else:
        return redirect(url_for("main"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if request.form.get('LoginPageButton'):
            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/main", methods=['GET', 'POST'])
def main():
    global Authed

    if Authed == False:
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.form.get('LogoutButton'):
            Authed = False
            return redirect(url_for("login"))

    return render_template("main.html")



if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)