from flask import Blueprint, jsonify, request
from .models import Todo, db

bp = Blueprint('api', __name__)

### The API route will be for the new vue version of the site
# A route to fetch the list of my projects (json endpoint)
@bp.route('/api/projects')
def api_projects():
	projects = [
		{ 'id': 1, 'name': 'Meowdy', 'desc': 'A cute random cat project', 'url': 'https://en.wikipedia.org/wiki/Cat'},
		{ 'id': 2, 'name': 'Astro-Synth', 'desc': 'Procedural synth in C++/Raylib', 'url': 'https://github.com/vena/astro-synth' },
		{ 'id': 3, 'name': 'Rat-Synth', 'desc': 'The Gays', 'url': 'https://github.com/vena/astro-synth' }
	]
	return jsonify({ 'projects': projects })