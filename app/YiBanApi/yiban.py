# coding=utf-8
from flask import current_app,request,redirect,session
from Crypto.Cipher import AES
import json
import urllib2
from ..utils.error import error


class YiBanApi:
    @classmethod
    def oauth(cls):
        oauth_url='https://openapi.yiban.cn/oauth/authorize?client_id=%s&redirect_uri=%s&state=mobile' % (
            current_app.config.get('APP_ID'), current_app.config.get('APP_URL'))

        if 'verify_request' not in request.args:
            return redirect(oauth_url)
        verify_request = request.args.get('verify_request')
        base_info=cls.base_info(verify_request)
        session['base_info']=base_info
        print base_info

    @classmethod
    def detail_info(cls):
        """
        :return:
        {
        "yb_money": "351010",
        "yb_usernick": "\u8def\u4eba\u7532",
        "yb_schoolname": "\u91cd\u5e86\u5927\u5b66",
        "yb_regtime": "2015-07-23 11:43:18",
        "yb_userhead": "http://img02.fs.yiban.cn/5559093/avatar/user/200",
        "yb_userid": "5559093",
        "yb_schoolid": "527",
        "yb_sex": "M",
        "yb_username": "\u8def\u4eba\u7532",
        "yb_exp": "5925"
}

        or False
        """
        token = session['base_info']['access_token']
        res = urllib2.urlopen(url='https://openapi.yiban.cn/user/me?access_token=%s' % token).read()
        detail_info = json.loads(res)
        print "res:", detail_info
        if detail_info and detail_info['status'] == 'success':
            return detail_info['info']
        else:
            return error('获取详细信息出错！')


    @staticmethod
    def h2b(s):
        import array, string
        ar = array.array('c')
        start = 0
        if s[:2] == '0x':
            start = 2
        for i in range(start, len(s), 2):
            num = string.atoi("%s" % (s[i:i + 2],), 16)
            ar.append(chr(num))
        return ar.tostring()

    @classmethod
    def decrypt(cls, verify_request):
        """
        {
            "visit_oauth": {
                "access_token": "5a5595d4869d5afca35fefe89fb4a3d14f085be1",
                "token_expires": 1489940242
            },
            "visit_time": 1488642455,
            "visit_user": {
                "username": "0x5f3759df",
                "usernick": "0x5f3759df",
                "usersex": "M",
                "userid": "5566213"
            }
        }
        """
        try:
            mode = AES.MODE_CBC
            data = YiBanApi.h2b(verify_request)
            decryptor = AES.new(current_app.config.get('APP_SECRET'), mode, IV=current_app.config.get('APP_ID'))
            plain = decryptor.decrypt(data)
            oauth_state = json.loads(plain.rstrip(chr(0)))
            return oauth_state
        except Exception as e:
            print e
            return False

    @classmethod
    def base_info(cls, verify_request):
        """
                    鑾峰彇鏄撶彮鎺堟潈鐨勫熀鏈俊鎭�
                    :return: {
                        'access_token': 瑙佹槗鐝紑鍙戞枃妗�,
                        'username': 鏄撶彮鐢ㄦ埛鍚�,
                        'usernick': 鏄撶彮鐢ㄦ埛鍚�,
                        'usersex': 鏄撶彮鐢ㄦ埛鎬у埆,
                        'userid': 鏄撶彮鐢ㄦ埛ID,
                        'visit_time': 鎺堟潈鏃堕棿
                     }
                     or False
                    """
        user_info = cls.decrypt(verify_request)
        if user_info:
            try:
                base_info = {
                    'access_token': user_info['visit_oauth']['access_token'],
                    'username': user_info['visit_user']['username'],
                    'usernick': user_info['visit_user']['usernick'],
                    'usersex': user_info['visit_user']['usersex'],
                    'userid': user_info['visit_user']['userid'],
                    'visit_time': user_info['visit_time']
                }
                return base_info
            except Exception as e:
                print e
                return False
        return False
