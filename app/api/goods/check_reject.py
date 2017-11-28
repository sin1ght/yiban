# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session,request
from app.decorators import login_required
from app.models import User,Good


@api.route('/goods/check_reject')
@login_required
def goods_check_reject():
    flag = request.args.get('flag')
    reason = request.args.get('reason')
    if not (flag and reason):
        return error('提交参数不合法')

    s_userid = flag.split('#', 1)[0]
    s_createtime = flag.split('#', 1)[1]

    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    if user.status == 1:
        progress = 1
    elif user.status == 2:
        progress = 2
    else:
        return error('学生权限不够')

    good = Good.query.filter(Good.user_id == s_userid,Good.create_time == s_createtime).first()
    if not good:
        return error('不存在此申请')
    good.update(verify_res=1, progress=progress, reason=reason)
    return success({'msg': '审核通过成功', 'good': good.to_json()})