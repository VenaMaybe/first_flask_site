from flask import Flask, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)

# Storing data here for now!
todos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo/')
def todo():
    return render_template('todo.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    new_todo = request.form['todo']
    todos.append(new_todo)
    return redirect(url_for('todo'))

@app.route('/remove/<int:todo_id>')
def remove(todo_id):
    if 0 <= todo_id < len(todos):
        del todos[todo_id]
    return redirect(url_for('todo'))

@app.route('/art/')
def art():
    return render_template('art.html')

@app.route('/posts/')
def posts():
    # Access the template folder path
    # template_directory = app.template_folder
    posts_directory = os.path.join(app.root_path, 'templates/posts')
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

@app.route('/debug-paths/')
def debug_paths():
    posts_directory = os.path.join(app.root_path, 'templates/posts')
    return {
        'root_path': app.root_path,
        'template_folder': app.template_folder,
        'computed_template_path': os.path.abspath(app.template_folder),
        'posts_directory': posts_directory  
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)