from flask import Flask, render_template
from ics import Calendar
import requests


app = Flask(__name__)

@app.route('/')
def index():
    url = "https://mobile-web.hr.nl/icalendar/calendar.ics?token=def74e319f2f49cf9352fef2bd3477e006906c7aff614f93bbeb7aa6c14e45b7"
    c = Calendar(requests.get(url).text)
    events = list(c.events)
    return render_template('index.html', events=events)
