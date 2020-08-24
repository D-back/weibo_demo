from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from libs.orm import db
from user.models import User

user_bp = Blueprint('user',__name__,url_prefix='/user')
user_bp.template_folder = './templates'


#注册页面
@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        city = request.form.get('city')
        phone = request.form.get('phone')

        try:
            User.query.filter_by(username=username).one()
            return '用户名已存在'
        except Exception:
            user = User(username=username, password=password,
                        gender=gender, city=city, phone=phone)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')

    else:
        return render_template('register.html')

@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).one()
            if user.password == password:
                session['usernme'] = username
                return redirect('/user/info')
            else:
                return '密码错误'
        except Exception:
            return '您还没有注册，请先注册'


    else:
        return render_template('login.html')