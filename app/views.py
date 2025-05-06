from flask import Blueprint, render_template, current_app
from jinja2 import TemplateNotFound
import os

bp = Blueprint('views', __name__)

@bp.route('/')
def index():
	return render_template('index.html')

### New Site Landing
@bp.route('/new-landing')
def new_landing():
	return render_template('new-landing.html')

@bp.route('/art')
def art():
	return render_template('art.html')

@bp.route('/doesntExist')
def doesntExist():
	return render_template('doesntExist.html')

### Posts:

@bp.route('/posts')
def posts():
	# Access the template folder path
	# template_directory = app.template_folder
	posts_directory = os.path.join(current_app.template_folder, 'posts')
	print('\n\n\n\n')
	print('Directory path:', posts_directory)
	# Assume all post templates are stored in 'templates/posts/'
	# Adjust the path according to your project structure
	try:
		post_files = os.listdir(posts_directory)  # Lists all files in the posts directory
		# Create a list of dictionaries with display names and file names
		posts = [{'display': post.replace('.html', '').replace('_', ' '),
				  'link': post.replace('.html', '')} 
				 for post in post_files if post.endswith('.html')]
	except FileNotFoundError:
		posts = []  # No posts directory found, or other file read error

	return render_template('posts.html', posts=posts)

@bp.route('/posts/<post_name>')
def post(post_name):
	try:
		return render_template(f'posts/{post_name}.html')
	except TemplateNotFound:
		print("uwuwuwuuwuw\n\n\n\n")
		return render_template('doesntExist.html'), 404

@bp.route('/debug-paths')
def debug_paths():
	posts_directory = os.path.join(bp.root_path, 'templates/posts')
	return {
		'root_path': bp.root_path,
		'template_folder': bp.template_folder,
		'computed_template_path': os.path.abspath(bp.template_folder),
		'posts_directory': posts_directory  
	}

