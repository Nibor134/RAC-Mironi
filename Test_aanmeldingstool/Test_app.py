import sqlite3
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, send_file, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from lib.classes import *

# Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

login_manager = LoginManager(app)
login_manager.login_view = "login"
    
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM Studenten WHERE id = (?)",[user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2])

#Main Route  
@app.route("/", methods=['GET','POST'])
def redirectpage():
    return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM Studenten WHERE studentnummer = (?)",    [form.studentnummer.data])
        user = list(curs.fetchone())
        Us = load_user(user[0])
        if form.studentnummer.data == Us.studentnummer and form.password.data == Us.password:
            login_user(Us, remember=form.remember.data)
            Umail = list({form.studentnummer.data})[0].split('@')[0]
            flash('Logged in successfully '+Umail)
            redirect(url_for('main'))
        else:
            flash('Login Unsuccessfull.')
    if request.method == "POST": 
        if request.form.get('SignupPageButton'):
            return redirect(url_for("signup"))
        elif request.form.get('HomeButton'):
            return redirect(url_for("login"))

    return render_template('login.html',title='Login', form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if request.form.get('LoginPageButton'):
            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if request.form.get('LogoutButton'):
            Authed = False
            return redirect(url_for("login"))

    return render_template("main.html")



if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)