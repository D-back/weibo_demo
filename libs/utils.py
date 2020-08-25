import os
from hashlib import md5,sha256

from flask import session
from flask import render_template

def make_password(password):
    '''产生一个安全密码'''
    if not isinstance(password,bytes):
        password = str(password).encode('utf8')

    #计算哈希值
    hash_value = sha256(password).hexdigest()

    #产生随机盐，长度32字节
    salt = os.urandom(16).hex()

    #加盐，产生安全密码
    safe_password = salt + hash_value

    return safe_password

def check_password(password,safe_password):
    '''检查密码'''
    if not isinstance(password,bytes):
        password = str(password).encode('utf8')

    hash_value = sha256(password).hexdigest()
    return hash_value == safe_password[32:]





#判断是否已登录
def login_required(view_func):
    def check_sess(*args,**kwargs):
        username = session.get('username')
        if not username:
            return render_template('login.html',err='您还没有登录，请先登录')
        else:
            return view_func(*args,**kwargs)
    return check_sess