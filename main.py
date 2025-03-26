from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.users import User
from data.jobs import Jobs
from data import jobs_api
from data import users_api
from data import jobs_resource
from data import users_resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


def main():
    db_session.global_init("db/mars_explorer.db")

    # Регистрация Blueprint API
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)

    # Регистрация RESTful ресурсов
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')

    app.run()


if __name__ == '__main__':
    main()