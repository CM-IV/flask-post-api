from logging import debug
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import date
import os


app = Flask(__name__)
dbDir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dbDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Post class/model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    publishDate = db.Column(db.TIMESTAMP, default=date.today())
    author = db.Column(db.String(50))
    alt = db.Column(db.String(50))

    def __init__(self, title, description, author, alt):
        self.title = title
        self.description = description
        self.author = author
        self.alt = alt

# Post schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'publishDate', 'author', 'alt')

# Init schema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


# Create a post
@app.route('/post', methods=['POST'])
def add_Post():
    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    alt = request.json['alt']

    new_post = Post(title, description, author, alt)

    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post)


# Fetch all posts
@app.route('/post', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result)

# Fetch one post
@app.route('/post/<id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    return post_schema.jsonify(post)

# Update a post
@app.route('/post/<id>', methods=['PUT'])
def update_Post(id):
    post = Post.query.get(id)

    title = request.json['title']
    description = request.json['description']
    author = request.json['author']
    alt = request.json['alt']

    post.title = title
    post.description = description
    post.author = author
    post.alt = alt

    db.session.commit()

    return post_schema.jsonify(post)

# Delete a post
@app.route('/post/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    
    return post_schema.jsonify(post)


# Run server
if __name__ == '__main__':
    app.run(debug=True)