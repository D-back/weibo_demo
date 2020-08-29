import datetime
from math import ceil

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import abort

from libs.orm import db
from libs.utils import login_required
from article.models import Arcitle
from article.models import Comment
from article.models import Thumb
from user.models import Follow

article_bp = Blueprint('article', __name__, url_prefix='/article')
article_bp.template_folder = './templates'


# 发表动态接口
@article_bp.route('/create', methods=('POST', 'GET'))
@login_required
def create_art():
    if request.method == 'POST':
        uid = session.get('uid')
        content = request.form.get('content')
        create_time = datetime.datetime.now()
        updated = datetime.datetime.now()

        if content:
            article = Arcitle(uid=uid, content=content, create_time=create_time, updated=updated)
            db.session.add(article)
            db.session.commit()
            session['art_id'] = article.id
            return redirect(f'/article/show?art_id={article.id}')
        else:
            return render_template('publish_article.html', err='内容不能为空')

    else:
        return render_template('publish_article.html')


# 微博显示接口
@article_bp.route('/show')
def show():
    art_id = int(request.args.get('art_id'))
    article = Arcitle.query.get(art_id)

    # 判断自己是否点过赞
    uid = session.get('uid')
    if uid:
        if Thumb.query.filter_by(wid=art_id, uid=uid).count():
            is_thumb = True
        else:
            is_thumb = False
    else:
        is_thumb = False

    # 判断评论内容是否为空
    err = request.args.get('err')
    if err:
        return render_template('show.html', article=article, err=err)
    else:
        # 获取当前微博所有的评论
        comments = Comment.query.filter_by(wid=art_id, is_delete=0).order_by(Comment.create_time.desc())
        return render_template('show.html', article=article, comments=comments, is_thumb=is_thumb)


# 修改动态接口
@article_bp.route('/modify', methods=('POST', 'GET'))
@login_required
def modify():
    if request.method == 'POST':
        art_id = request.form.get('art_id')
        content = request.form.get('content', )
        article = Arcitle.query.filter_by(id=art_id).one()

        if content:
            article.content = content
            article.updated = datetime.datetime.now()
            db.session.commit()
            session['art_id'] = art_id
            return redirect(f'/article/show?art_id={art_id}')
        else:
            uid = int(session.get('uid'))
            articles = Arcitle.query.filter_by(uid=uid).order_by(Arcitle.create_time.desc()).all()
            return render_template('modify.html', articles=articles, err='内容不能为空')

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
        start, end = 1, min(7, per_page)
    elif page > per_page - 3:
        start, end = per_page - 6, per_page
    else:
        start, end = page - 3, page + 3
    page_num = range(start, end + 1)
    articles = Arcitle.query.order_by(Arcitle.create_time.desc()).limit(30).offset(30 * (page - 1))
    return render_template('show_all.html', articles=articles, page=page,
                           page_num=page_num, max_page=per_page)


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


# 评论接口&回复接口
@article_bp.route('/comment_art', methods=('POST',))
def comment_art():
    if request.method == 'POST':
        uid = session.get('uid')
        cid = int(request.form.get('cid', '0'))
        wid = request.form.get('art_id')
        content = request.form.get('content')
        now = datetime.datetime.now()

        if content:
            comment = Comment(wid=wid, uid=uid, content=content, create_time=now, cid=cid)
            db.session.add(comment)
            db.session.commit()
            return redirect(f'/article/show?art_id={wid}')
        else:
            return redirect(f'/article/show?art_id={wid}&err=评论内容不能为空')
    else:
        abort(403)


# 删除评论接口
@article_bp.route('/delete_cmt')
def delete_cmt():
    cid = int(request.args.get('cid'))
    cmt = Comment.query.get(cid)

    # 检查是否是在删除别人的评论
    if cmt.uid != session['uid']:
        abort(403)

    # 修改数据
    cmt.is_delete = 1
    db.session.commit()

    return redirect('/')


# 点赞接口
@article_bp.route('/thumb')
@login_required
def thumb():
    uid = session.get('uid')
    wid = int(request.args.get('wid'))

    # 判断是否是再次点赞
    try:
        thumb = Thumb.query.filter_by(uid=uid, wid=wid).one()
        # 取消点赞
        if thumb:
            Thumb.query.filter_by(uid=uid, wid=wid).delete()
            Arcitle.query.filter_by(id=wid).update({'n_thumb': Arcitle.n_thumb - 1})
            db.session.commit()
    except Exception:
        # 提交点赞
        thumb = Thumb(uid=uid, wid=wid)
        db.session.add(thumb)
        Arcitle.query.filter_by(id=wid).update({'n_thumb': Arcitle.n_thumb + 1})
        db.session.commit()

    return redirect(f'/article/show?art_id={wid}')


#查看所有关注的人的微博
@article_bp.route('/fw_article')
@login_required
def fw_art():
    uid = session.get('uid')
    fw = Follow.query.filter_by(uid=uid).values('fid')
    fid_list = [fid for (fid,) in fw]
    articles = Arcitle.query.filter(Arcitle.uid.in_(fid_list)).order_by(Arcitle.updated.desc()).limit(100)
    return render_template('fw_article.html',articles=articles)


# # 热门微博
# @article_bp.route('/hot_art')
# def hot_art():
