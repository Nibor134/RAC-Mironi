# Route to create new class
from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import sqlite3

student_route = Blueprint('student_route', __name__)

@student_route.route('/check_in', methods=['GET', 'POST'])
def check_in():
    if 'student_logged_in' in session:
        return render_template('checkin.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))
    
