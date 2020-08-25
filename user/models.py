from libs.orm import db


class User(db.Model):
    """创建User表格"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.Enum('男', '女'), default='男')
    city = db.Column(db.String(20), default='上海')
    phone = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
