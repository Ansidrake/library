from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os 
load_dotenv()
from flask_migrate import Migrate



 # db intitialized here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY']  = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
#db.init_app(app)

#migrate = Migrate(app, db)

import model
import routes