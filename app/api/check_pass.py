# coding=utf-8
from . import api
from ..decorators import login_required
from flask import request,session
from ..models import Assessment,User
from ..utils.success import success
from ..utils.error import error


@api.route('/check_pass')
@login_required
def check_pass():
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    flag = request.args.get('flag')

    if not flag:
        return error('提交参数不合法')

    if '#' not in flag:
        return error('提交参数不合法')

    s_userid = flag.split('#', 1)[0]
    s_createtime = flag.split('#', 1)[1]

    if user.status == 1:
        return y_check(s_userid,s_createtime)
    elif user.status == 2:
        return x_check(s_userid,s_createtime)
    else:
        return error('学生权限不够')


#院老师
def y_check(s_userid,s_createtime):
    progress = 1
    assessment = Assessment.query.filter(Assessment.user_id==s_userid,Assessment.create_time==s_createtime).first()
    if not assessment:
        return error('不存在此文件')
    assessment.update(verify_res=2, progress=progress, reason='')

    return success({'msg': '审核通过成功', 'assessment': assessment.to_json()})


#校老师
def x_check(s_userid,s_createtime):
    progress = 2
    assessment = Assessment.query.filter(Assessment.user_id==s_userid,Assessment.create_time==s_createtime).first()
    if not assessment:
        return error('不存在此文件')
    assessment.update(verify_res=2, progress=progress, reason='')

    return success({'msg': '审核通过成功', 'assessment': assessment.to_json()})