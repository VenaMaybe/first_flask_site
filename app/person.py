from flask import Blueprint, request, jsonify, session
from .models import Person, NodeType, Node
from datetime import datetime
from . import db

bp = Blueprint('people', __name__)

@bp.route('/', methods=['POST'])
def create_person():
    user_id = session.get('user_id')
    if not user_id:
        return {'error': 'unauthorized'}, 401

    print(user_id)

    data = request.json
    # 1) find node_type for 'person'
    nt = NodeType.query.filter_by(type_of_node='person').first()
    if not nt:
        return {'error': 'NodeType "person" not found'}, 400

    # 2) create Node row
    node = Node(node_type_id=nt.id, created_by=user_id)  # or user_id if you like
    db.session.add(node)
    db.session.flush()  # so node.id exists

    # 3) create Person
    # Make sure birthday formatted correctly
    birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()

    person = Person(
        id=node.id,
        name=data['name'],
        email=data['email'],
        birthday=birthday,
        owner_user_id=user_id,
    )
    db.session.add(person)
    db.session.commit()
    return jsonify({'id': person.id, 'name': person.name}), 201

@bp.route('/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get_or_404(person_id)
    return jsonify({
        'id':        person.id,
        'name':      person.name,
        'email':     person.email,
        'owner':     person.owner_user_id
    })
