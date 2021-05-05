# From Flask OAuth Clients
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

@app.route('/')
def hello_user():
    return 'Welcome!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)



