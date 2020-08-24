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
            if title and content:
                article = Arcitle(title=title,content=content)
                db.session.add(article)
                db.session.commit()
                session['title'] = title
                return redirect('/article/show')
            else:
                return '标题和内容都不能为空'

        else:
            return render_template('publish_article.html')

