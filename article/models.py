import random

from libs.orm import db
from user.models import User
from libs.utils import random_zh_str


class Arcitle(db.Model):
    __tablename__ = 'article'
    '''创建文章的表'''

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)
    n_thumb = db.Column(db.Integer, nullable=False, default=0)

    # 获取用户的UID
    @property
    def author(self):
        return User.query.get(self.uid)

    # 创建随机动态
    @classmethod
    def fake_weibo(cls, uid_list, num):
        wb_list = []
        for i in range(num):
            year = random.randint(2000, 2019)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            data = '%04d-%02d-%02d' % (year, month, day)

            uid = random.choice(uid_list)
            content = random_zh_str(random.randint(70, 140))
            wb = cls(uid=uid, content=content, create_time=data, updated=data)
            wb_list.append(wb)

        db.session.add_all(wb_list)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comment'
    ''' 创建评论动态表'''

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    wid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True, default=0)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    is_delete = db.Column(db.Integer, default=0)

    # 获取当前评论的作者
    @property
    def author(self):
        return User.query.get(self.uid)

    @property
    def upper(self):
        '''上一级评论'''
        if self.cid == 0:
            return None
        else:
            return Comment.query.get(self.cid)


class Thumb(db.Model):
    __tablename__ = 'thumb'
    '''创建点赞表'''
    uid = db.Column(db.Integer, nullable=False, primary_key=True)
    wid = db.Column(db.Integer, nullable=False, primary_key=True)
