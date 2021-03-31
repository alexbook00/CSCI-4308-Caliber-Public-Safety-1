from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def Index():
    return render_template('index.html', message = "Jinja message from flask")
