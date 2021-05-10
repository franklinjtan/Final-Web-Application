from urllib import request
from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import requests

app = Flask(__name__, template_folder='templates')
app.secret_key = 'ying wu college 2021 secret key'


oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='290202919562-2qd67u9ko2016ijo95f2no2ssa3a4bs6.apps.googleusercontent.com',
    client_secret='poHIJ00YY61YC8g4yh1QGjfV',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def hello_user():
    email = dict(session).get('email', None)
    return f'Hello, {email} this is the main page!'


@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)