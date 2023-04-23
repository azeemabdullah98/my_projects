from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#Helper Table...
tags = db.Table('post_tag',
                db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
                db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),unique=True,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    tags = db.relationship('Tag',secondary=tags,backref=db.backref('post',lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tagname = db.Column(db.String(255))

    def __repr__(self):
        return "<Tag>-{}".format(self.tagname)


if __name__ == "__main__":
    app.run(debug=True)