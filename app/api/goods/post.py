# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session,request
from app.models import Good,User
from app.utils.stu_verify import get_stu_academy
from app.decorators import login_required


@api.route('/goods/post')
@login_required
def goods_post():
    name = request.args.get('name')
    category = request.args.get('category')
    num = request.args.get('num')
    last_time=request.args.get('last_time')
    stu_num = request.args.get('stu_num')
    s_academy = request.args.get('academy')

    if not (name and category and num and stu_num and s_academy and last_time):
        return error('提交参数不合法')

    academy = None
    if get_stu_academy(stu_num) and len(stu_num) == 8:
        academy = get_stu_academy(stu_num)
    else:
        return error('学号不符合规范')

    if academy != s_academy:
        return error('学号与学院不符合')

    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    good=Good(academy,name,category,num,last_time,user)
    good.save()

    return success('提交申请成功')