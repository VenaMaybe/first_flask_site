from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

load_dotenv()

db       = SQLAlchemy()
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins="*")

def create_app():
	# point template_folder at the sibling templates/ directory
	project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	template_dir = os.path.join(project_root, 'templates')
	static_dir   = os.path.join(project_root, 'static')

	app = Flask(
		__name__,
		template_folder=template_dir,
		static_folder=static_dir
	)

	app.config['SECRET_KEY']                = os.getenv('SECRET_KEY')
	app.config['SQLALCHEMY_DATABASE_URI']   = os.getenv('DATABASE_URL')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	# config
	app.url_map.strict_slashes = False

	db.init_app(app)
	socketio.init_app(app)

	# register blueprints
	from .auth          import bp as auth_bp;          app.register_blueprint(auth_bp)
	from .api           import bp as api_bp;           app.register_blueprint(api_bp, url_prefix='/api')
	from .sockets       import init_sockets;           init_sockets(socketio)
	from .views         import bp as views_bp;         app.register_blueprint(views_bp)
	from .time_tracker  import bp as tt_bp;            app.register_blueprint(tt_bp, url_prefix='/time-tracker')
	from .todo          import bp as todo_bp;          app.register_blueprint(todo_bp, url_prefix='/todo')

	return app
