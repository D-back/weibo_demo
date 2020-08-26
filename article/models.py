from libs.orm import db
from user.models import User


class Arcitle(db.Model):
    """创建文章的表"""
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer,nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,nullable=False)
    updated = db.Column(db.DateTime,nullable=False)

    #获取用户的UID
    @property
    def author(self):
        return User.query.get(self.uid)