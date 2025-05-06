from flask import Blueprint, redirect, url_for, session, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
import os

bp = Blueprint('auth', __name__)

#	in prod : export OAUTHLIB_INSECURE_TRANSPORT=1
#
#

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

@bp.route("/api/user")
def user_info():
	if not google.authorized:
		return {"logged_in": False}, 401
	resp = google.get("/oauth2/v2/userinfo")
	resp.raise_for_status()
	profile = resp.json()
	return {
		"logged_in": True,
		"id": profile["id"],
		"email": profile["email"],
		"name": profile["name"],
		"first": profile["given_name"],
		"last": profile["family_name"],
		"picture": profile["picture"]
	}

@bp.route("/login")
def login():
	return redirect(url_for("auth.google.login"))

@bp.route("/api/test-user")
def test_user():
	if not google.authorized:
		return "❌ User not logged in", 401

	# fetch the profile from Google
	resp = google.get("/oauth2/v2/userinfo")
	resp.raise_for_status()
	profile = resp.json()

	# print to your Flask console
	print("🟢 Logged-in user profile:", profile)

	# return it as JSON so you can inspect in the browser or curl
	return jsonify(profile)

@bp.route('/logout')
def logout():
    # remove the Flask-Dance token from the session
    session.pop('google_oauth_token', None)
    # if you’re storing anything else—like your own user ID—pop it too:
    # session.pop('user_id', None)
    # now send them back to your home or login page
    return redirect(url_for('index'))  # or 'new_landing' or wherever