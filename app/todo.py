from flask import Blueprint, render_template, request, jsonify
from flask_socketio import emit
from .models import Todo, db
from . import socketio

bp = Blueprint('todo', __name__)

# An in memory cache
todos = [];
next_id = 1

# lock map
locks = {}
currently_dragged_todos = {} #A shared map of what's being dragged!

# Init from db
def load_todos_from_db():
	global todos, next_id
	todos = [todo.to_dict() for todo in Todo.query.order_by(Todo.position).all()]
	next_id = max([todo['id'] for todo in todos], default=0) + 1

# Create database and table
@bp.before_request
def init_todos():
	db.create_all()
	load_todos_from_db()

@bp.route('/')
def index():
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
	
	socketio.emit('update', {
		'todos': todos,
		'locks': locks
	})

@bp.route('/add', methods=['POST'])
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

@bp.route('/remove', methods=['POST'])
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

@bp.route('/update-id-location', methods=['POST'])
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

@bp.route('/update-order', methods=['POST'])
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

