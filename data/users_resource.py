from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({
            'user': user.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position',
                'speciality', 'address', 'email'))
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position',
                'speciality', 'address', 'email')) for item in users]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        if session.query(User).filter(User.email == args['email']).first():
            abort(400, message=f"User with email {args['email']} already exists")

        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        user.set_password(args['password'])

        session.add(user)
        session.commit()
        return jsonify({'id': user.id})