from flask import redirect, url_for, session, jsonify
from flask_dance.contrib.google import google
from . import bp			# blueprint
from ..models import User	# the database object
from .. import db			# the database

@bp.route("/login")
def login():
	return redirect(url_for("auth.google.login"))

@bp.route("/api/user")
def user_info():
	if not google.authorized:
		return {"logged_in": False}, 401
	
	# ── fetch profile from Google ─────────────────────────
	resp = google.get("/oauth2/v2/userinfo")
	resp.raise_for_status()
	profile = resp.json()

	# ── find or create our local User ────────────────────
	local_user = User.query.filter_by(google_id=profile["id"]).first()
	if not local_user:
		local_user = User(
			google_id  = profile["id"], # even though "id" it is from google!
			email      = profile["email"],
			name       = profile["name"],
			first_name = profile["given_name"],
			last_name  = profile["family_name"],
			picture    = profile["picture"]
		)
		db.session.add(local_user)
		db.session.commit()

	# ── save local user id in session ────────────────────
	session["user_id"] = local_user.id # This is not the google ID!!!

	# ── return whatever the frontend needs ────────────────
	return {
		"logged_in": True,
		"id": profile["id"],
		"email": profile["email"],
		"name": profile["name"],
		"first": profile["given_name"],
		"last": profile["family_name"],
		"picture": profile["picture"]
	}

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
    session.pop('user_id', None)
    # now send them back to your home or login page
    return redirect(url_for('views.index'))  # or 'new_landing' or wherever