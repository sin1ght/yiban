# coding=utf-8

from . import oauth
from ..YiBanApi.yiban import YiBanApi
from flask import redirect,url_for,session
from ..models import User,Teacher


@oauth.route('/')
def index():
    if YiBanApi.oauth():
        return YiBanApi.oauth()

    base_info=session['base_info']
    userid=base_info['userid']

    user=User.query.filter_by(id=userid).first()
    if not user:
        academy=None #学院
        status=0 #用户身份类型:0 is 学生，1 is 院易班指导老师 2 is 校易班指导老师
        detail_info=YiBanApi.detail_info()
        teacher=Teacher.query.filter_by(id=userid).first()
        if teacher:
            academy=teacher.academy
            print 'academy'+academy
            status=teacher.status
        user=User(userid,detail_info['yb_sex'],detail_info['yb_usernick'],detail_info['yb_userhead'],None,academy,status)
        user.save()

    if user.status == 0:
        return redirect(url_for('main_blueprint.stu_index'))
    else:
        return redirect(url_for('main_blueprint.tea_index'))



