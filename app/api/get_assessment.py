# coding=utf-8
from . import api
from ..utils.success import success
from ..utils.error import error
from ..models import Assessment,User
from flask import session
from ..decorators import login_required


@api.route('/get_assessment')
@login_required
def get_assessment():
    userid = session['base_info']['userid']
    user = User.query.filter_by(id=userid).first()

    if user.status == 1:
        return y_get(user)
    elif user.status == 2:
        return x_get()
    else:
        return error('学生没有权限')


def y_get(user):
    '''院老师'''
    assessments = [assessment.to_json() for assessment in Assessment.query.filter(Assessment.progress==0,Assessment.academy==user.academy ).all()]
    return success(assessments)


def x_get():
    '''校老师'''
    assessments = [assessment.to_json() for assessment in Assessment.query.filter(Assessment.progress==1,Assessment.verify_res==2).all()]
    return success(assessments)