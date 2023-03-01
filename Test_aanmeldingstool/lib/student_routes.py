# Route to create new class
from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import requests
import sqlite3
from icalendar import Calendar

student_route = Blueprint('student_route', __name__)

@student_route.route('/check_in', methods=['GET', 'POST'])
def check_in():
    if 'student_logged_in' in session:
        return render_template('checkin2.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))
    
@student_route.route('/rooster')
def rooster():
    # Haal de ics file op vanaf de URL
    url = 'https://roosterapi.hr.nl/timetables/personalized/0909114/export'
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
        event_start = event.get('dtstart').dt
        event_end = event.get('dtend').dt
        events.append({
            'summary': event_summary,
            'location': event_location,
            'description': event_description,
            'start': event_start,
            'end': event_end
        })

    # Geef de verwerkte ics gegevens door aan de template
    return render_template('rooster.html', events=events)

@student_route.route('student/upcoming_meetings')
def s_upcoming_meetings():
    return render_template('student_upcoming_meetings.html')

@student_route.route('/checkin/<int:meeting_id>', methods=['GET'])
def checkin_page(meeting_id):
    # Render the check-in page with the meeting ID
    return render_template('checkin2.html', meeting_id=meeting_id)
