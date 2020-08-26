import datetime
from math import ceil
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
        uid = session.get('uid')
        content = request.form.get('content')
        create_time = datetime.datetime.now()
        updated = datetime.datetime.now()

        if  content:
            article = Arcitle(uid=uid,content=content, create_time=create_time,updated=updated)
            db.session.add(article)
            db.session.commit()
            session['art_id'] = article.id
            return redirect('/article/show')
        else:
            return render_template('publish_article.html', err='内容不能为空')

    else:
        return render_template('publish_article.html')


# 微博显示接口
@article_bp.route('/show')
def show():
    art_id = session.get('art_id')
    article = Arcitle.query.get(art_id)
    return render_template('show.html', article=article)


# 修改动态接口
@article_bp.route('/modify', methods=('POST', 'GET'))
@login_required
def modify():
    if request.method == 'POST':
        art_id = int(request.form.get('art_id'))
        content = request.form.get('content',)
        article = Arcitle.query.filter_by(id=art_id).one()

        if content:
            article.content = content
            article.updated = datetime.datetime.now()
            db.session.commit()
            session['art_id'] = art_id
            return redirect('/article/show')
        else:
            uid = int(session.get('uid'))
            articles = Arcitle.query.filter_by(uid=uid).order_by(Arcitle.create_time.desc()).all()
            return render_template('modify.html', articles=articles,err='内容不能为空')

    else:
        uid = int(session.get('uid'))
        articles = Arcitle.query.filter_by(uid=uid).order_by(Arcitle.create_time.desc()).all()
        return render_template('modify.html', articles=articles)


# 显示所有动态
@article_bp.route('/show_all')
def show_all():
    page = int(request.args.get('page', 1))
    count_articles = Arcitle.query.count()
    per_page = ceil(count_articles / 30)

    if page <= 3:
        start, end = 1, 7
    elif page > per_page - 3:
        start, end = per_page - 6, per_page
    else:
        start, end = page - 3, page + 3
    page_num = range(start, end + 1)
    articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(30).offset(30 * (page - 1))
    return render_template('show_all.html', articles=articles, page=page, page_num=page_num)


# 删除动态接口
@article_bp.route('/delete')
def delete_art():
    art_id = int(request.args.get('art_id'))
    Arcitle.query.filter_by(id=art_id).delete()
    db.session.commit()

    art_id = session.get('art_id')
    if not art_id:
        pass
    else:
        session.pop('art_id')
    return redirect('/')
