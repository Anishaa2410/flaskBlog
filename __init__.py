from flask_sqlalchemy import *
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) 


app.config['SECRET_KEY'] = 'CViN8EDaSjq7VrTlaLccig'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db=SQLAlchemy(app)
bcr= Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category = 'danger'
from flaskblog import routes