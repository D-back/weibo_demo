import datetime
import random

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from libs.orm import db
from libs.utils import login_required
from article.models import Arcitle

article_bp = Blueprint('article', __name__, url_prefix='/article')
article_bp.template_folder = './templates'


# 发表动态接口
@article_bp.route('/create', methods=('POST', 'GET'))
@login_required
def create_art():
    # 产生随机动态
    # title = ''
    # content = ''
    # name = [chr(x) for x in range(10000,18000)]
    # for i in range(1,80):
    #     for x in range(1,16):
    #         title += random.choice(name)
    #     for z in range(1,30):
    #         content += random.choice(name)
    #     create_time = datetime.datetime.now()
    #     article = Arcitle(title=title, content=content, create_time=create_time)
    #     db.session.add(article)
    #     db.session.commit()
    #     title = ''
    #     content = ''

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        create_time = datetime.datetime.now()
        if title and content:
            article = Arcitle(title=title, content=content, create_time=create_time)
            db.session.add(article)
            db.session.commit()
            session['title'] = title
            return redirect('/article/show')
        else:
            return render_template('publish.html', err='标题和内容都不能为空')

    else:
        return render_template('publish_article.html')


# 微博显示接口
@article_bp.route('/show')
def show():
    title = session.get('title')
    if not title:
        return redirect('/article/create')
    else:
        article = Arcitle.query.filter_by(title=title).one()
        return render_template('show.html', article=article)


# 修改动态接口
@article_bp.route('/modify', methods=('POST', 'GET'))
# @login_required
def modify():
    if request.method == 'POST':
        art_id = int(request.form.get('id'))
        title = request.form.get('title')
        content = request.form.get('content')
        article = Arcitle.query.filter_by(id=art_id).one()
        article.title = title
        article.content = content
        db.session.commit()
        session['title'] = title
        return redirect('/article/show')
    else:
        username = session.get('username')
        if not username:
            return render_template('login.html', err='您还没有登录，请先登录')
        else:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).all()
            return render_template('modify.html', articles=articles)


# 显示所有动态
@article_bp.route('/show_all')
def show_all():
    username = session.get('username')
    if not username:
        return render_template('login.html', err='您还没有登录，请先登录')
    else:
        num = request.args.get('num')
        count_articles = (Arcitle.query.order_by(Arcitle.create_time.desc())).count()
        page_num = count_articles // 30
        syts = count_articles % 30

        if not num:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(30)
            return render_template('show_all.html', articles=articles, num=2)
        elif int(num) <= page_num:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(30).offset(30 * (int(num) - 1))
            return render_template('show_all.html', articles=articles, num=int(num) + 1)
        elif page_num < int(num) <= page_num + 1:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(syts).offset(30 * (int(num) - 1))
            return render_template('show_all.html', articles=articles, num=int(num) + 1)
        elif int(num) > page_num + 1:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(syts).offset(30 * (int(num) - 2))
            return render_template('show_all.html', articles=articles, err='已经是最后一页')



# 删除动态接口
@article_bp.route('/delete')
def delete_art():
    art_id = int(request.args.get('art_id'))
    Arcitle.query.filter_by(id=art_id).delete()
    db.session.commit()

    title = session.get('title')
    if not title:
        pass
    else:
        session.pop('title')
    return redirect('/')
