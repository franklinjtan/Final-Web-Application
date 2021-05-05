# From Flask OAuth Clients
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
oauth = OAuth(app)
google = oauth.register(
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
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize:
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    return redirect('/')

