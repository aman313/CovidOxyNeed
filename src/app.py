import sqlite3
from flask import Flask, render_template, request, redirect
from utilities.db_connection import DbConnection
app = Flask(__name__)


@app.route('/')
def index():
    db = DbConnection.get_connection()
    return render_template('index.html')
