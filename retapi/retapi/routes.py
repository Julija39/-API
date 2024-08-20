from flask import request, jsonify
from flask_restful import Resource
from models import db, User, Post
from db import db


class PostResource(Resource):
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if post:
                return jsonify({"id": post.id, "title": post.title, "content": post.content, "author": post.author.username})
            return {"message": "Post not found"}, 404
        else:
            posts = Post.query.all()
            return jsonify([{"id": post.id, "title": post.title, "content": post.content, "author": post.author.username} for post in posts])

    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {"message": "User not found"}, 404
        new_post = Post(title=data['title'], content=data['content'], author=user)
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post created", "post_id": new_post.id}, 201

    def put(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {"message": "Post not found"}, 404
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return {"message": "Post updated"}

    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return {"message": "Post not found"}, 404
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}



class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify({"id": user.id, "username": user.username})
            return {"message": "User not found"}, 404
        else:
            users = User.query.all()
            return jsonify([{"id": user.id, "username": user.username} for user in users])

    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {"message": "Username already exists"}, 400
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "user_id": new_user.id}, 201

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}

def initialize_routes(api):
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(PostResource, '/posts', '/posts/<int:post_id>')

