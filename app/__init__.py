from flask import Flask, send_from_directory, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager, create_access_token
from flask_migrate import Migrate
from flask_restful import Api

from app.api import ClientsResource, ClientResource, OrdersResource, OrderResource
from app.models import db, Order, Client, User


def send_client(filename='index.html'):
    return send_from_directory('static', filename)


def login():
    username = request.json.get("username", None)
    user = User.query.filter_by(username=username).first()
    password = request.json.get("password", None)
    if not user or not user.hash_verify(password):
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'abc'
    app.config['JWT_SECRET_KEY'] = 'abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Lab2.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_envvar('APP_CONFIG', True)

    db.init_app(app)
    Migrate(app, db, render_as_batch=('sqlite' in app.config['SQLALCHEMY_DATABASE_URI']))

    admin = Admin(app)
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(Client, db.session))

    JWTManager(app)

    app.add_url_rule('/login/', view_func=login, methods=['POST'])
    app.add_url_rule('/', view_func=send_client)
    app.add_url_rule('/<path:filename>', view_func=send_client)

    api = Api(app)
    api.add_resource(ClientsResource, '/client/')
    api.add_resource(ClientResource, '/client/<int:client_id>/')

    api.add_resource(OrdersResource, '/order/')
    api.add_resource(OrderResource, '/order/<int:order_id>/')

    return app