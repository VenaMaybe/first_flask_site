from . import db

# Define the todo model
class Todo(db.Model):
	__tablename__ = 'todos'
	id         = db.Column(db.Integer, primary_key=True)
	text       = db.Column(db.String(255), nullable=False)
	position   = db.Column(db.Integer, nullable=False)

	def to_dict(self):
		return {'id': self.id, 'text': self.text}