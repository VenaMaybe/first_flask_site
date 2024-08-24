from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from datetime import datetime # [USE : TIME TRACKER]
import os

app = Flask(__name__)
#app.url_map.strict_slashes = False # Doesn't force the absense of / after url
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # Use later for login sessions?
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # Might want to check if is None later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')

### Slash Remover
@app.before_request
def remove_trailing_slash():
    path = request.path
    # If the request path ends with a slash but is not the root path, redirect
    if path != '/' and path.endswith('/'):
        return redirect(path.rstrip('/'), code=301) # Code for SEO silliness

### Time tracker
@app.route('/time-tracker')
def time_tracker():
	return render_template('time-tracker.html')

last_state_time = datetime.now()

@app.route('/time-tracker/state', methods=['POST'])
def time_tracker_state_update():
	global last_state_time

	state = request.get_json().get('state')
	current_state_time = datetime.now()

	difference_state_time = current_state_time - last_state_time;

	# Extract hours, minutes, and seconds from the timedelta
	total_seconds = difference_state_time.total_seconds()
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)

	# Format the difference as HH:MM:SS
	formatted_difference = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

	print(state, datetime.now().strftime("%I:%M:%S %p"), ' difference: ', formatted_difference)

	last_state_time = datetime.now()
	return jsonify({"status": "state changed", "time_difference": formatted_difference})




### Todos:

# Define the todo model
class Todo(db.Model):
	__tablename__ = 'todos'
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(255), nullable=False)
	position = db.Column(db.Integer, nullable=False)

	def to_dict(self):
		return {'id': self.id, 'text': self.text}

# Init from db
def load_todos_from_db():
	global todos, next_id
	todos = [todo.to_dict() for todo in Todo.query.order_by(Todo.position).all()]
	next_id = max([todo['id'] for todo in todos], default=0) + 1

# Create database and table
with app.app_context():
	db.create_all()
	load_todos_from_db()

# Storing data here for now!
#todos = []
#next_id = 1
locks = {}
currently_dragged_todos = {} #A shared map of what's being dragged!

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/todo')
def todo():
	print('Rendering order:', todos)
	load_todos_from_db() # Refreshes todo from db for localhost & vps
	return render_template('todo.html', todos=todos)

def emit_todo_update():
	global todos

#	Todo.query.delete()
#	db.session.commit()
#
#	for i, todo in enumerate(todos):
#		db_todo = Todo(id=todo['id'], text=todo['text'], position=i)
#		db.session.add(db_todo)
#	
#	db.session.commit()
	
	print("Todos:")
	for todo in todos:
		print(todo)
	
	socketio.emit('update', {'todos': todos, 'locks': locks})

@app.route('/add', methods=['POST'])
def add():
	global next_id, todos
	new_todo_text = request.form['todo']
	new_todo = {'id': next_id, 'text': new_todo_text, 'position': len(todos)}
	todos.append(new_todo)
	next_id += 1

	#db stuff
	db_todo = Todo(id=new_todo['id'], text=new_todo['text'], position=new_todo['position'])
	db.session.add(db_todo)
	db.session.commit()

	emit_todo_update()
	return jsonify({'status': 'success', 'todo': new_todo})

@app.route('/remove', methods=['POST'])
def remove():
	global todos
	todo_id = request.json['todo_id']

	print("Currently dragged: ", currently_dragged_todos)

	if str(todo_id) in currently_dragged_todos:
		emit_todo_update()
		return jsonify({'status': 'failure', 'message': 'Todo is currently being dragged and cannot be removed'}), 400

	todos = [todo for todo in todos if todo['id'] != todo_id]

	# Update the database
	Todo.query.filter_by(id=todo_id).delete()
	db.session.commit()
			# This happens a little bit slower than ui update

	emit_todo_update()
	return jsonify({'status': 'success', 'todos': todos})

@app.route('/update-id-location', methods=['POST'])
def update_id_location():
	data = request.json
	todoId = int(data.get('itemId'))
	newIndex = int(data.get('newIndex'))

	todo = next((item for item in todos if item['id'] == todoId), None)		
	
	if todo:
		todos.remove(todo)
		if newIndex < len(todos):
			todos.insert(newIndex, todo)
		else:
			todos.append(todo)

		# Update positions in the database
		for i, todo in enumerate(todos):
			db_todo = db.session.get(Todo, todo['id'])
			db_todo.position = i
		db.session.commit()

		# Emit the updated to-do list to all clients
		emit_todo_update()

		return jsonify({'status': 'success', 'id': todoId, 'newIndex': newIndex})
	return jsonify({'status': 'error', 'message': 'Todo not found'}), 404

@socketio.on('start_drag')
def handle_start_drag(data):
	print('\tStart Drag, received data:', data)
	item_id = data['itemId']
	parent_id = data['parentId']
	currently_dragged_todos[item_id] = parent_id
	emit('update_dragged_elements_start', currently_dragged_todos, broadcast=True)
	print('cdt', currently_dragged_todos)

@socketio.on('end_drag')
def handle_end_drag(data):
	print('\tEnd Drag')
	item_id = data['itemId']
	if item_id in currently_dragged_todos:
		del currently_dragged_todos[item_id]
	emit('update_dragged_elements_end', currently_dragged_todos, broadcast=True)
	print('cdt', currently_dragged_todos)

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

###
#
#

@app.route('/art')
def art():
	return render_template('art.html')

@app.route('/doesntExist')
def doesntExist():
	return render_template('doesntExist.html')

### Posts:

@app.route('/posts')
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

@app.route('/posts/<post_name>')
def post(post_name):
	try:
		return render_template(f'posts/{post_name}.html')
	except TemplateNotFound:
		print("uwuwuwuuwuw\n\n\n\n")
		return render_template('doesntExist.html'), 404

@app.route('/debug-paths')
def debug_paths():
	posts_directory = os.path.join(app.root_path, 'templates/posts')
	return {
		'root_path': app.root_path,
		'template_folder': app.template_folder,
		'computed_template_path': os.path.abspath(app.template_folder),
		'posts_directory': posts_directory  
	}

if __name__ == "__main__":
	socketio.run(app, debug=True, host='0.0.0.0', port=5000)
