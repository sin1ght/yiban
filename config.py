# coding=utf-8
import os

basedir=os.path.abspath(os.path.dirname(__file__))


class Config(object):

    HOST="http://127.0.0.1:5000"

    #易班配置
    APP_ID="7ba404619270b948"
    APP_SECRET="a183525404e08c2f4f13ef061a722eb9"
    APP_URL="http://f.yiban.cn/iapp141803"

    #app
    UPLOAD_FOLDER=os.path.join(basedir,'app\upload')
    SECRET_KEY = '3c8bbbdd9bf770459e7f32b490eccc9b'
    DEBUG=False
    SQLALCHEMY_DATABASE_URI=""


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'data.db')


config={
    'default':DevConfig
}

if __name__ == "__main__":
    print Config.UPLOAD_FOLDER