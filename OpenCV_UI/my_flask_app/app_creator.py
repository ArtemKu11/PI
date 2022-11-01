import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__) 



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)




