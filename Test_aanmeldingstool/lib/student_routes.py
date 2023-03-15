# Route to create new class
from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import requests
import sqlite3
from icalendar import Calendar
import pytz

student_route = Blueprint('student_route', __name__)
amsterdam_tz = pytz.timezone('Europe/Amsterdam')
# Student dashboard
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db', check_same_thread=False)
c = conn.cursor()

@student_route.route('/student_dashboard')
def student_dashboard(events=[]):
    if 'student_logged_in' in session:
        c.execute('SELECT student_name FROM Students WHERE Studentnumber = ?', (session['username'],))
        name_s = c.fetchone()[0]
        username = session.get('username')
        url = f'https://roosterapi.hr.nl/timetables/personalized/{username}/export'
        response = requests.get(url)
        ics_content = response.text
        cal_data = response.content.decode('utf-8')
        # Verwerk de ics file met behulp van icalendar module
        cal = Calendar.from_ical(cal_data)
        events = []
        for event in cal.walk('VEVENT'):
            event_summary = event.get('summary')
            event_location = event.get('location')
            event_description = event.get('description')
            event_start_utc = event.get('dtstart').dt
            event_end_utc = event.get('dtend').dt
            event_start_amsterdam = event_start_utc.astimezone(amsterdam_tz)
            event_end_amsterdam = event_end_utc.astimezone(amsterdam_tz)
            event_start = event_start_amsterdam.strftime('%Y-%m-%d %H:%M:%S')
            event_end = event_end_amsterdam.strftime('%Y-%m-%d %H:%M:%S')
            events.append({
                'summary': event_summary,
                'location': event_location,
                'description': event_description,
                'start': event_start,
                'end': event_end
            })
        return render_template('student_dashboard.html', name_s=name_s, events=events)
    else:
        flash('Ongeldige inloggegevens.', 'danger')
        return redirect(url_for('login'))

@student_route.route('/rooster')
def rooster():
    if 'student_logged_in' in session:
        # Haal de ics file op vanaf de URL
        username = session.get('username')
        url = f'https://roosterapi.hr.nl/timetables/personalized/{username}/export'
        response = requests.get(url)
        ics_content = response.text
        cal_data = response.content.decode('utf-8')
        # Verwerk de ics file met behulp van icalendar module
        cal = Calendar.from_ical(cal_data)
        events = []
        for event in cal.walk('VEVENT'):
            event_summary = event.get('summary')
            event_location = event.get('location')
            event_description = event.get('description')
            event_start_utc = event.get('dtstart').dt
            event_end_utc = event.get('dtend').dt
            event_start_amsterdam = event_start_utc.astimezone(amsterdam_tz)
            event_end_amsterdam = event_end_utc.astimezone(amsterdam_tz)
            event_start = event_start_amsterdam.strftime('%Y-%m-%d %H:%M:%S')
            event_end = event_end_amsterdam.strftime('%Y-%m-%d %H:%M:%S')
            events.append({
                'summary': event_summary,
                'location': event_location,
                'description': event_description,
                'start': event_start,
                'end': event_end
            })

        # Geef de verwerkte ics gegevens door aan de template
        return render_template('rooster.html', events=events)
    else:
        flash('Log alstublieft eerst in', 'danger')
    return redirect(url_for('login'))

@student_route.route('/student/upcoming_meetings')
def s_upcoming_meetings():
    return render_template('student_upcoming_meetings.html')

@student_route.route('/checkin/<int:meeting_id>', methods=['GET'])
def check_in(meeting_id):
    if 'student_logged_in' in session:
        print(session)
        return render_template('checkin2.html', meeting_id=meeting_id)
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login_for_redirect', meeting_id=meeting_id))
