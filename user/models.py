import random

from libs.orm import db
from libs.utils import random_zh_str

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
    avatar = db.Column(db.String(256),default='/static/img/default.png')


    #创建随机用户
    @classmethod
    def fake_users(cls,num):
        users = []
        for i in range(num):
            username = random_zh_str(3)
            password = '123456'
            gender = random.choice(['男','女'])
            phone = '123456789'
            create_time = '2000-01-21'
            user = cls(username=username,password=password,gender=gender,
                       phone=phone,create_time=create_time)
            users.append(user)

        db.session.add_all(users)
        db.session.commit()
        return users