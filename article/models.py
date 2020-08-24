from libs.orm import db

class Arcitle(db.Model):
    """创建文章的表"""
    __tablename__ = 'article'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime)