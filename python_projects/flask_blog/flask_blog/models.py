from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_blog import login_manager,db,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email},'{self.image_file}')"

# class Tag(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     tagname = db.Column(db.Text)

#     def __init__(self,tagname):
#         self.tagname = tagname

#     def __repr__(self):
#         return f"Tag(tagname={self.tagname})"

# tags = db.Table('posts_tag',
#                 db.Column('blogposts_id',db.Integer,db.ForeignKey('post.id'),nullable=False),
#                 db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'),nullable=False))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # tags = db.relationship('Tag',secondary=tags,backref=db.backref('blogpost',lazy='dynamic'))

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

