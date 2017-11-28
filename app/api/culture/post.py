# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session,request
from app.models import CulProduct,User
from app.utils.stu_verify import get_stu_academy
from app.decorators import login_required


@api.route('/culture_product/post')
@login_required
def culture_product_post():
    name=request.args.get('name')
    category=request.args.get('category')
    num=request.args.get('num')
    stu_num = request.args.get('stu_num')
    s_academy = request.args.get('academy')

    if not (name and category and num and stu_num and s_academy):
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

    cul_product=CulProduct(academy,name,category,num,user)
    cul_product.save()

    return success('提交成功')