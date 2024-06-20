from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from jinja2 import TemplateNotFound
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Storing data here for now!
todos = []

next_id = 1 #Unique IDs for items!
locks = {}
currently_dragged_todos = {} #A shared map of what's being dragged!

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/todo/')
def todo():
	print('Rendering order:', todos)
	return render_template('todo.html', todos=todos)

def emit_todo_update():
	
	print("Todos:")
	for todo in todos:
		print(todo)
	
	socketio.emit('update', {'todos': todos, 'locks': locks})

@app.route('/add', methods=['POST'])
def add():
	global next_id
	new_todo_text = request.form['todo']
	new_todo = {'id': next_id, 'text': new_todo_text}
	todos.append(new_todo)
	next_id += 1
	emit_todo_update()
	return jsonify({'status': 'success', 'todo': new_todo})

@app.route('/remove/<int:todo_id>', methods=['POST'])
def remove(todo_id):
	global todos
	todos = [todo for todo in todos if todo['id'] != todo_id]
	emit_todo_update()
	return jsonify({'status': 'success'})

@app.route('/update-id-location', methods=['POST'])
def update_id_location():
	data = request.json
	todoId = int(data.get('id'))
	newIndex = int(data.get('newIndex'))

	todo = next((item for item in todos if item['id'] == todoId), None)		
	
	todos.remove(todo)
	if newIndex < len(todos):
		todos.insert(newIndex, todo)
	else:
		todos.append(todo)
	
	# Emit the updated to-do list to all clients
	emit_todo_update()

	return jsonify({'status': 'success', 'id': todoId, 'newIndex': newIndex})

@socketio.on('start_drag')
def handle_start_drag(data):
	print('Start Drag, received data:', data)
	item_id = data['id']
	parent_id = data['parentId']
	currently_dragged_todos[item_id] = parent_id
	emit('update_dragged_elements', currently_dragged_todos, broadcast=True)

@socketio.on('end_drag')
def handle_end_drag(data):
	print('End Drag')
	item_id = data['id']
	if item_id in currently_dragged_todos:
		del currently_dragged_todos[item_id]
	emit('update_dragged_elements', currently_dragged_todos, broadcast=True)


@app.route('/update-order', methods=['POST'])
def update_order():
	order = request.json.get('order')

	if not order:
		return jsonify({'status': 'failure', 'message': 'No order provided'}), 400

	try:
		# You have to do this to access global variables!
		global todos

		# Create a mapping of ID to to-do item
		id_to_todo = {todo['id']: todo for todo in todos}

		# Reorder the todos based on the provided order
		new_todos = [id_to_todo[int(todo_id)] for todo_id in order]

		todos = new_todos

		# Emit the updated to-do list to all clients
		emit_todo_update()

		return jsonify({'status': 'success', 'new_order': todos})
	except KeyError as e:
		error_message = f'Invalid to-do ID in order: {str(e)}'
		print('Error:', error_message)
		return jsonify({'status': 'failure', 'error': error_message}), 400
	except Exception as e:
		print('Error:', str(e))
		return jsonify({'status': 'failure', 'error': str(e)}), 400

@socketio.on('lock')
def handle_lock(data):
	todo_id = data['todoId']
	locks[todo_id] = True
	emit('lock', {'todoId': todo_id}, broadcast=True)
	print('\nLocking: ', todo_id, ' locks now: ', locks)

@socketio.on('unlock')
def handle_unlock(data):
	todo_id = data['todoId']
	if todo_id in locks:
		del locks[todo_id]
	print('\nUnlocking', todo_id, ' locks now: ', locks)
	emit('unlock', {'todoId': todo_id}, broadcast=True)

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
	app.run(debug=True, host='0.0.0.0', port=5000)