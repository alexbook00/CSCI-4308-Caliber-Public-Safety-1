from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory, send_file, safe_join, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import json

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
    dashboard = db.Column(db.Text)
    
#flask-login call back funtion to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#flask-login call back function for Unauth users 
@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html', Message = "Unauthorized user please log in.")

@app.route('/')
def login():
    return render_template('login.html')

#fuction run when user hits submit on login page
@app.route('/loginuser', methods=['POST','GET'])
def loginuser():
    username = request.form['username']#pull username and password from html
    password = request.form['password']
    user = User.query.filter_by(username=username).first() #query sqllite for username
    try:
        if user.username == username and password == user.password:
            login_user(user)
            return redirect(url_for('index'))
    except:
        return render_template('login.html', Message = 'Incorrect username or password.')
    return render_template('login.html', Message = 'Incorrect username or password.')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html', Message = 'You are now logged out.')
    

@app.route('/index')
@login_required
def index():
    if current_user.username == "CaliberAdmin":
        thisDashboard = User.query.all()
        # print(users)
        # thisDashboard = {}
        # for user in users:
        #     if user.username != "CaliberAdmin":
        #         thisDashboard = {**thisDashboard, **json.loads(user.dashboard)}
    elif current_user.is_authenticated:
        thisDashboard = json.loads(current_user.dashboard)
    return render_template('index.html', Dashboards = thisDashboard)

@app.route('/edit')
@login_required
def edit():
    if current_user.is_authenticated:
        thisDashboard = json.loads(current_user.dashboard)
    return render_template('edit.html', Dashboards = thisDashboard)



@app.route('/remove',  methods=['POST'])
@login_required
def remove():
    Name = request.form['dashboardName']
    Dashboards = getDashboardsDictionary()
    del Dashboards[Name]
    commitDictionaryToDatabase(Dashboards)
    return render_template('edit.html', Dashboards=Dashboards)


@app.route('/editusers',  methods=['POST','GET'])
@login_required
def editusers():
    if current_user.username != "CaliberAdmin":
        return redirect(url_for('index'))
    username = request.form['username']
    password = request.form['password']
    userID = request.form['userID']
    if request.method == 'POST':
        if request.form['submit_button'] == 'change':
            print(username, password, userID)
            changeUserInfo(userID, username, password)
        elif request.form['submit_button'] == 'remove':
            removeUser(userID)
    return render_template('index.html', Dashboards=User.query.all())


@app.route('/adduser',  methods=['POST', 'GET'])
@login_required
def adduser():
    if current_user.username != "CaliberAdmin":
        return redirect(url_for('index'))
    username = request.form['username']
    password = request.form['password']
    users = User.query.all()
    for user in users:
        if user.username == username:
            return render_template('index.html', Dashboards=User.query.all(), Message="Username already exists.")
    addNewUser(username, password)
    return render_template('index.html', Dashboards=User.query.all())

@app.route('/newdash',  methods=['POST'])
@login_required
def newdash():
    newName = request.form['dashboardName']
    newURL = request.form['powerBIURL']
    Dashboards = getDashboardsDictionary()
    if newName not in Dashboards.keys():
        Dashboards[newName] = newURL
        commitDictionaryToDatabase(Dashboards)
    else:
        return render_template('edit.html', Message= "Dashboards Can't Share the same name.", Dashboards = Dashboards)
    return render_template('edit.html', Dashboards = Dashboards)

############# Helper Fucntions #############   
def getDashboardsDictionary():
    if current_user.is_authenticated:
        Dashboards = json.loads(current_user.dashboard)
    return Dashboards

def DictionaryToJSON(Dictionary):
    JSON = json.dumps(Dictionary)
    return JSON
    
def commitDictionaryToDatabase(Dictionary):
    JSON = DictionaryToJSON(Dictionary)
    current_user.dashboard = JSON
    db.session.commit()

def changeUserInfo(userID, username, password):
    users = User.query.all()
    user = User.query.filter_by(id = userID).first()
    user.username = username
    user.password = password
    db.session.commit()

def addNewUser(username, password):
    newuser = User(username=username, password=password, dashboard=DictionaryToJSON({"DashBoard Name Placeholder": "https://ThisIsAPlaceHolderURL.fake"}))
    db.session.add(newuser)
    db.session.commit()

def removeUser(userID):
    User.query.filter_by(id = userID).delete()
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)