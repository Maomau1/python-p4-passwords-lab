#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user = User.query.filter(User.id == session['user_id']).first()
        if user:
            return user.to_dict(), 200
        else:
            return {}, 204
api.add_resource(CheckSession, '/check_session')

class Login(Resource):
    def post (self):
        user = User.query.filter(
            User.username == request.get_json()['username']).first()
        password = request.get_json()['password']

        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid username or password'}, 401
api.add_resource(Login, '/login')

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {'message': '204: No content'}, 204
api.add_resource(Logout, '/logout')

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
