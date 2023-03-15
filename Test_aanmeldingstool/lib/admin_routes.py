from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import datetime
import sqlite3
import socket

admin = Blueprint('admin', __name__)