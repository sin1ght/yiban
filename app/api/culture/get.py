# coding=utf-8
from .. import api
from app.utils.success import success
from app.utils.error import error
from flask import session
from app.decorators import login_required
from app.models import User,CulProduct


@api.route('/culture_product/get')
@login_required
def culture_product_get():
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    if user.status==1:
        return y_get(user)
    elif user.status==2:
        return x_get()
    else:
        return error('学生没有权限')


#院老师
def y_get(user):
    products = [product.to_json() for product in
                CulProduct.query.filter(CulProduct.progress == 0,CulProduct.academy == user.academy).all()]
    return success(products)


#校老师
def x_get():
    cul_products = [cul_product.to_json() for cul_product in
                    CulProduct.query.filter(CulProduct.verify_res==2,CulProduct.progress == 1).all()]
    return success(cul_products)