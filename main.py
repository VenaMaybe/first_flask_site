from flask import Flask, render_template
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)

DEV_MODE = True
if DEV_MODE:
    app.root_path = ""

@app.route('/')
def index():
    template_path = os.path.join(app.root_path, 'templates', 'index.html')
    return render_template('index.html')

@app.route('/art/')
def art():
    return render_template('art.html')

@app.route('/testfile/')
def testfile():
    # template_directory = app.template_folder
    posts_directory = os.path.join(app.root_path, 'posts')
    try:
        with open(posts_directory + '/Test_Post_One.html', 'r') as file:
            content = file.read()
            return content  # This will display the file content in the browser
    except Exception as e:
        return str(e)  # Display the error in the browser

@app.route('/debug-paths/')
def debug_paths():
    return {
        'root_path': app.root_path,
        'template_folder': app.template_folder,
        'computed_template_path': os.path.abspath(app.template_folder)
    }

@app.route('/posts/')
def posts():
    # Access the template folder path
    # template_directory = app.template_folder
    posts_directory = os.path.join(app.root_path, 'posts')
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

@app.route('/doesntExist/')
def doesntExist():
    return render_template('doesntExist.html')

@app.route('/posts/<post_name>')
def post(post_name):
    try:
        return render_template(f'posts/{post_name}.html')
    except TemplateNotFound:
        print("uwuwuwuuwuw\n\n\n\n")
        return render_template('doesntExist.html'), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)