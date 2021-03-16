from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory, send_file, safe_join, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)

if os.name == "nt":
    db_file_path = 'sqlite:////' + os.path.dirname(os.path.realpath(__file__)) + "\login.db"
else:
    db_file_path = 'sqlite:////' + os.path.dirname(os.path.realpath(__file__)) + "/login.db"
app.config['SQLALCHEMY_DATABASE_URI'] = db_file_path
app.config['SECRET_KEY'] = 'sd65fg62fd6'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#flask-login User class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

#flask-login call back funtion to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#flask-login call back function for Unauth users 
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html', Message = "Unauthorized user please log in.")

#fuction run when user hits submit on login page
@app.route('/loginuser', methods=['POST','GET'])
def loginuser():
    #pull username and password from html
    username = request.form['username']
    password = request.form['password']
    #query sqllite for username
    user = User.query.filter_by(username=username).first()
    Realpassword =  User.query.filter_by(password=username).first()
    #Check username and password
    if not user:
        return render_template('login.html', Message = 'User not found.')
    if password != Realpassword :
        return render_template('login.html', Message = 'Wrong password.')
    login_user(user)
    return redirect(url_for('index'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html')