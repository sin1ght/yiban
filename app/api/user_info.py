from . import api
from ..utils.success import success
from flask import session
from ..models import User
from ..decorators import login_required


@api.route('/user_info')
@login_required
def user_info():
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    assessments=[assessment.to_json() for assessment in user.assessments.all()]
    info=user.to_json()
    info['assessments']=assessments

    cul_products=[cul_product.to_json() for cul_product in user.culproducts.all()]
    info['cul_products']=cul_products

    goods=[good.to_json() for good in user.goods.all()]
    info['goods']=goods
    return success(info)