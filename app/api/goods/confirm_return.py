# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session,request
from app.decorators import login_required
from app.models import User,Good


@api.route('/goods/confirm_return')
@login_required
def goods_confirm_return():
    flag = request.args.get('flag')
    if not flag:
        return error('提交参数不合法')
    s_userid = flag.split('#', 1)[0]
    s_createtime = flag.split('#', 1)[1]

    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    if user.status != 0:
        return error('只有学生有权限')

    good = Good.query.filter(Good.user_id == s_userid, Good.create_time == s_createtime).first()
    if not good:
        return error('不存在此申请')
    good.update(is_lend_return=2)
    return success('确认归还成功')