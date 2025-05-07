import os
from flask import Blueprint
from flask_dance.contrib.google import make_google_blueprint

bp = Blueprint('auth', __name__)

# using https://console.cloud.google.com/auth/overview?project=connections-v1&supportedpurview=project
### Tell flask-dance client creds
google_bp = make_google_blueprint(
	client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
	client_secret=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
	scope=[
      "openid",
      "https://www.googleapis.com/auth/userinfo.email",
      "https://www.googleapis.com/auth/userinfo.profile",
    ],
	redirect_url="http://localhost:5173/connections/welcome"
)
bp.register_blueprint(google_bp, url_prefix="/login")

# import the routes
from . import routes