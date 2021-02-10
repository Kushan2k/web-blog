from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_login import LoginManager



app=Flask(__name__)
app.config['SECRET_KEY']='06507d45c78802f66ae9055cf32d0e74c24519d9'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

login_magager=LoginManager(app)

from webblog import route