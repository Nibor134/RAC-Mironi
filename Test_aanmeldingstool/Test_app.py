import sqlite3
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, send_file, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from lib.classes import LoginForm, User
from lib.tablemodel import DatabaseModel
import os.path



# Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True


app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

DATABASE_FILE = os.path.join(app.root_path, 'databases', 'test_database2.db')
dbm = DatabaseModel(DATABASE_FILE)

login_manager = LoginManager(app)
login_manager.login_view = "login"

def connect_to_db():
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database2.db')
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database2.db')
    curs = conn.cursor()
    curs.execute("SELECT * from Users where id = (?)",[user_id])
    lu = curs.fetchone()
    if lu is None:
      return None
    else:
      return User(int(lu[0]), lu[1], lu[2])

#Main Route  
@app.route("/", methods=['GET','POST'])
def redirectpage():
    return redirect(url_for("login"))

# Login Route
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard'))
  form = LoginForm()
  if form.validate_on_submit():
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database2.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM Users where username = (?)",    [form.username.data])
    user = curs.fetchone()
    Us = load_user(user[0])
    if form.username.data == Us.username and form.password.data == Us.password:
        login_user(Us)
        return redirect(('dashboard'))
    else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)

# Signup Route
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        if request.form.get('LoginPageButton'):
            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    #if request.method == "POST":
        #if request.form.get('LogoutButton'):
            #Authed = False
            #return redirect(url_for("login"))

    return render_template("main.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")

@app.route("/registration")
def registration():
    rows, columns = dbm.get_table_content('Studenten')
    return render_template("registration.html", rows=rows, columns=columns)

@app.route("/presence")
def presence():
    return redirect("presence")

@app.route("/student")
def student():
    return redirect("student")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("login")

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)