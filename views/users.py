from flask import request
from flask_restx import Namespace, Resource

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = db.session.query(User).all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        req_json.pop("id", None)
        new_user = User(**req_json)
        db.session.add(new_user)
        db.session.commit()
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = db.session.query(User).get(uid)
        res = UserSchema().dump(user)
        return res, 200

    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")

        db.session.add(user)
        db.session.commit()
        return "", 204
