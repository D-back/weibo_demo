import datetime

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from libs.orm import db
from article.models import Arcitle

article_bp = Blueprint('article', __name__, url_prefix='/article')
article_bp.template_folder = './templates'


#发表动态接口
@article_bp.route('/create',methods=('POST','GET'))
def create_art():
    username = session.get('username')
    if not username:
        return '请先登录'
    else:
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            create_time = datetime.datetime.now()
            if title and content:
                article = Arcitle(title=title,content=content,create_time=create_time)
                db.session.add(article)
                db.session.commit()
                session['title'] = title
                return redirect('/article/show')
            else:
                return '标题和内容都不能为空'

        else:
            return render_template('publish_article.html')

#微博显示接口
@article_bp.route('/show')
def show():
    title = session.get('title')
    if not title:
        return redirect('/article/create')
    else:
        article = Arcitle.query.filter_by(title=title).one()
        return render_template('show.html',article=article)


#修改动态接口
@article_bp.route('/modify',methods=('POST','GET'))
def modify():
    if request.method == 'POST':
        art_id = int(request.form.get('id'))
        title = request.form.get('title')
        content = request.form.get('content')
        article = Arcitle.query.filter_by(id=art_id).one()
        article.title = title
        article.content = content
        db.session.commit()
        session['title']=title
        return redirect('/article/show')
    else:
        username = session.get('username')
        if not username:
            return '请先登录'
        else:
            articles = Arcitle.query.order_by(Arcitle.create_time.desc()).all()
            return render_template('modify.html',articles=articles)

#删除动态接口
@article_bp.route('/delete')
def delete_art():
    art_id = int(request.args.get('art_id'))
    Arcitle.query.filter_by(id=art_id).delete()
    db.session.commit()

    title = session.get('title')
    if  not title:
        pass
    else:
        session.pop('title')
    return redirect('/')