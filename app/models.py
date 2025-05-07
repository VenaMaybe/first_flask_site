from . import db
# for utcnow
from datetime import datetime, timezone

# Define the todo model
class Todo(db.Model):
    __tablename__ = 'todos'
    id         = db.Column(db.Integer, primary_key=True)
    text       = db.Column(db.String(255), nullable=False)
    position   = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'text': self.text}
#####################################################3


# Store each logged-in user!
#	Ties a google identity to a local record
class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.BigInteger, primary_key=True)
    google_id     = db.Column(db.String(64), unique=True, nullable=False)
    email         = db.Column(db.String(255), unique=True, nullable=False)
    name          = db.Column(db.String(150), nullable=False)
    first_name    = db.Column(db.String(100))
    last_name     = db.Column(db.String(100))
    picture       = db.Column(db.String(500))
    created_at    = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        return f'<User {self.email}>'

class NodeType(db.Model):
    __tablename__ = 'node_types'

    id            = db.Column(db.BigInteger, primary_key=True)
    type_of_node  = db.Column(db.String(50), unique=True, nullable=False)
    def __repr__(self):
        return f'<NodeType {self.type_of_node}>'

class Node(db.Model):
    __tablename__ = 'nodes'

    id            = db.Column(db.BigInteger, primary_key=True)
    node_type_id  = db.Column(db.BigInteger, db.ForeignKey('node_types.id'), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by    = db.Column(db.BigInteger, db.ForeignKey('nodes.id'), nullable=True)

    # relationships
    node_type     = db.relationship('NodeType', backref='nodes')
    creator       = db.relationship('Node', remote_side=[id], backref='children')

class SocialAccount(db.Model):
	__tablename__ = 'social_accounts'

	id        = db.Column(db.BigInteger, db.ForeignKey('nodes.id'), primary_key=True)
	platform  = db.Column(db.String(50), nullable=False)
	handle    = db.Column(db.String(100), nullable=False)

	# relationship
	node = db.relationship('Node', backref=db.backref('social_account', uselist=False))

	def __repr__(self):
		return f'<SocialAccount {self.platform}:{self.handle}>'

class Person(db.Model):
    __tablename__ = 'persons'

    id             = db.Column(db.BigInteger, db.ForeignKey('nodes.id'), primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(255), nullable=False, unique=True)
    birthday       = db.Column(db.Date, nullable=False)
    owner_user_id  = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=True)

    # relationships
    node           = db.relationship('Node', backref=db.backref('person', uselist=False))
    owner          = db.relationship('User', backref='owned_persons')

class Connection(db.Model):
    __tablename__ = 'connections'

    id            = db.Column(db.BigInteger, primary_key=True)
    from_node_id  = db.Column(db.BigInteger, db.ForeignKey('nodes.id'), nullable=False)
    to_node_id    = db.Column(db.BigInteger, db.ForeignKey('nodes.id'), nullable=False)
    type          = db.Column(db.String(50), nullable=False)
    created_at    = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # relationships
    from_node     = db.relationship('Node', foreign_keys=[from_node_id], backref='connections_out')
    to_node       = db.relationship('Node', foreign_keys=[to_node_id],   backref='connections_in')

class ClaimRequest(db.Model):
    __tablename__ = 'claim_requests'

    id                = db.Column(db.BigInteger, primary_key=True)
    person_id         = db.Column(db.BigInteger, db.ForeignKey('persons.id'), nullable=False)
    requester_user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'),   nullable=False)
    target_user_id    = db.Column(db.BigInteger, db.ForeignKey('users.id'),   nullable=False)
    status            = db.Column(db.Enum('pending','approved','denied', name='claim_status'), default='pending', nullable=False)
    message           = db.Column(db.Text, nullable=True)
    created_at    = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    decided_at        = db.Column(db.DateTime, nullable=True)

    # relationships
    person            = db.relationship('Person', backref='claim_requests')
    requester         = db.relationship('User', foreign_keys=[requester_user_id], backref='requests_made')
    target            = db.relationship('User', foreign_keys=[target_user_id], backref='requests_to_approve')


