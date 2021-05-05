# From Flask OAuth Clients
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from auth_decorator import login_required
from dotenv import load_dotenv
load_dotenv()

# App config
app = Flask(__name__)
