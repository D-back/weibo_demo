from flask import Flask
from flask_script import Manager
from flask import render_template
from flask_migrate import Migrate,MigrateCommand

from libs.orm import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:961224@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = r'@$!@#RWRAE%#$%$s!3122ASf@#%#!%rfy(()'

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@app.route('/')
def home():
    return '测试页面'


if __name__ == '__main__':
    manager.run()