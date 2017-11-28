# coding=utf-8
from . import api
from ..decorators import login_required
from flask import request,session
from ..models import Assessment,User
from ..utils.success import success
from ..utils.error import error


@api.route('/check_reject')
@login_required
def check_reject():
        
    flag = request.args.get('flag')
    reason = request.args.get('reason')
    s_userid = flag.split('#', 1)[0]
    s_createtime = flag.split('#', 1)[1]
	
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()
	
    progress=0
    if user.status == 1:
        progress = 1
    elif user.status == 2:
        progress=2
    else:
        return error('学生权限不够')

    if flag and reason:
        assessment = Assessment.query.filter(Assessment.user_id == s_userid,Assessment.create_time == s_createtime).first()
        if not assessment:
            return error('不存在此文件')
        assessment.update(progress=progress,verify_res=1,reason=reason)

        return success({'msg': '审核驳回成功', 'assessment': assessment.to_json()})
    else:
        return error('提交参数不合法')
