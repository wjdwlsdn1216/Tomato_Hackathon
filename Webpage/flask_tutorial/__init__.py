from flask import Flask
from flask_sqlalchemy import SQLAlchemy #can use data classes as a python class
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

app = Flask(__name__) # name of module
app.config['SECRET_KEY']='0bb21b2c08b45e4b66e46eea9a782c2b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = 'info'

from flask_tutorial import routes