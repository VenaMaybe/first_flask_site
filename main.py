from flask import Flask, render_template
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/art/')
def art():
    return render_template('art.html')

@app.route('/testfile/')
def testfile():
    try:
        with open('templates/posts/Test_Post_One.html', 'r') as file:
            content = file.read()
            return content  # This will display the file content in the browser
    except Exception as e:
        return str(e)  # Display the error in the browser

@app.route('/posts/')
def posts():
    directory = os.path.abspath('templates/posts')
    print('Directory path:', directory)
    # Assume all post templates are stored in 'templates/posts/'
    # Adjust the path according to your project structure
    try:
        post_files = os.listdir(directory)  # Lists all files in the posts directory
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