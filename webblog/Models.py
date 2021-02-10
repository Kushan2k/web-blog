from datetime import datetime

from webblog import db,login_magager
from flask_login import UserMixin

@login_magager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user table for storing user in the database
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(50),unique=True,nullable=False)
    username=db.Column(db.String(10),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)
    profilepic=db.Column(db.String(30),default='')

    def __repr__(self):
        return f'User({self.username},{self.email})'

# post table for storing post in the database
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,default='')
    image=db.Column(db.String(40),default='')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    def __repr__(self):
        return f'Post({self.date},{self.content})'

