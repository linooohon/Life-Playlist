from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # 拿到當下時間
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 拿使用者 id 當 fk
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 拿使用者 id 當 fk
    test_migrate_col = db.Column(db.String(120), nullable=True) #預設就是 nullable=True 可以不寫

    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    # notes = db.relationship('Note', backref='user')

    def __init__(self, email, password, first_name):
        self.email = email
        self.password = password
        self.first_name = first_name
