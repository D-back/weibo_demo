import datetime

from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import render_template

from libs.orm import db
from libs.utils import login_required
from libs.utils import make_password
from libs.utils import check_password
from user.models import User

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.template_folder = './templates'


# 注册接口
@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password1 = request.form.get('password1','').strip()
        password2 = request.form.get('password2','').strip()
        gender = request.form.get('gender','').strip()
        city = request.form.get('city','').strip()
        phone = request.form.get('phone','').strip()
        now = datetime.datetime.now()
        try:
            User.query.filter_by(username=username).one()
            return render_template('register.html',err='用户名已存在')
        except Exception:
            if not password1 or password1 != password2:
                return render_template('register.html',err='密码不一致')
            user = User(username=username, password=make_password(password1),
                        gender=gender, city=city, phone=phone,create_time=now)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')

    else:
        return render_template('register.html')


# 登录接口
@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    username = session.get('username')
    if not username:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            try:
                user = User.query.filter_by(username=username).one()
                if check_password(password,user.password):
                    session['username'] = username
                    return redirect('/user/info')
                else:
                    return render_template('login.html',err='密码错误')

            except Exception:
                return render_template('register.html', err='请先注册')

        else:
            return render_template('login.html')
    else:
        return redirect('/user/info')

# 用户个人信息接口
@user_bp.route('/info')
@login_required
def info():
    username = session.get('username')
    # if not username:
    #     return '亲您还没有登录哦！请您先登录的呢。'
    # else:
    user = User.query.filter_by(username=username).one()
    return render_template('info.html', user=user)


# 退出接口
@user_bp.route('logout')
def logout():
    username = session.get('username')
    if not username:
        return render_template('login.html',err='您还没有登录，请先登录')

    else:
        session.pop('username')
        return redirect('/user/login')
