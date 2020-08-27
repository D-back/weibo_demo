from flask import Flask
from flask_script import Manager
from flask import redirect
from flask_migrate import Migrate, MigrateCommand

from libs.orm import db
from user.models import User
from article.models import Arcitle
from user.views import user_bp
from article.views import article_bp



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:961224@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = r'@$!@#RWRAE%#$%$s!3122ASf@#%#!%rfy(()'
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)
app.register_blueprint(article_bp)


@app.route('/')
def home():
    return redirect('/article/show_all')


@manager.command
def create_test_weibo():
    '''创建微博测试数据'''
    users = User.fake_users(50)
    uid_list = [u.id for u in users ]
    Arcitle.fake_weibo(uid_list,500)

if __name__ == '__main__':
    manager.run()
