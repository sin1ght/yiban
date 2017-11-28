# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session
from app.decorators import login_required
from app.models import User,Good


@api.route('/goods/get')
@login_required
def goods_get():
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    if user.status == 1:
        return y_get(user)
    elif user.status == 2:
        return x_get()
    else:
        return error('学生没有权限')


def y_get(user):
    goods=[good.to_json() for good in
           Good.query.filter(Good.progress==0,Good.academy==user.academy).all()]
    return success(goods)


def x_get():
    goods = [good.to_json() for good in
             Good.query.filter(Good.progress == 1, Good.verify_res==2).all()]
    return success(goods)