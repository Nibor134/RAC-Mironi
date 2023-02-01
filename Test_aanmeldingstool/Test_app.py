import sqlite3
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, send_file


# Flask Settings
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = 'Hogeschoolrotterdam'

#Main Route
@app.route("/")
def redirectpage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)