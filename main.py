from flask import Flask
from flask_script import Manager
from flask import redirect
from flask_migrate import Migrate,MigrateCommand

from libs.orm import db
from user.views import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:961224@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = r'@$!@#RWRAE%#$%$s!3122ASf@#%#!%rfy(()'
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

app.register_blueprint(user_bp)

@app.route('/')
def home():
    return redirect('/user/register')


if __name__ == '__main__':
    manager.run()