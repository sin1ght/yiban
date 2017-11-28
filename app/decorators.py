# coding=utf-8

from functools import wraps
from flask import current_app,session
from .utils.error import error


def login_required(f):
    @wraps(f)
    def decorated_func(*args,**kwargs):
        if 'base_info' not in session:
            # oauth_url = 'https://openapi.yiban.cn/oauth/authorize?client_id=%s&redirect_uri=%s&state=mobile' % (
            #     current_app.config.get('APP_ID'), current_app.config.get('APP_URL'))
            return error('未进行易班授权，请重新进入应用！')
        return f(*args,**kwargs)
    return decorated_func
