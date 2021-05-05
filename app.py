# From Flask OAuth Clients
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def hello_user():
    return 'Welcome!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize:
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    return redirect('/')

