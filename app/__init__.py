from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
Database settings
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.database import database
from app.views import views
from app.logic import statistics