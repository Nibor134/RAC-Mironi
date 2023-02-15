import sqlite3
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, send_file, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
 studentnummer = StringField('Studentnummer',validators=[DataRequired()])
 password = PasswordField('Password',validators=[DataRequired()])
 submit = SubmitField('Login')
 def validate_studentnummer(self, studentnummer):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
    curs = conn.cursor()
    curs.execute("SELECT studentnummer FROM Studenten where studentnummer = (?)",[studentnummer.data])
    valstudentnummer = curs.fetchone()
    if valstudentnummer is None:
      raise ValidationError('This studentnummer ID is not registered. Please register before login')

class User(UserMixin):
    def __init__(self, id, studentnummer, password):
         self.id = (id)
         self.studentnummer = studentnummer
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id