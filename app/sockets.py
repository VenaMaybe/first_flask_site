from flask_socketio import emit

def init_sockets(socketio):
	@socketio.on('draw_data')
	def handle_draw(data):
		# smt like {'x': cord, 'y': cord}
		emit('draw_data', data, broadcast=True, include_self=False)

