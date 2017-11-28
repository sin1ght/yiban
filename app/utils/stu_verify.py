#!/usr/bin/env python
# coding=utf-8
import hashlib

import re
import requests


class StuVerify:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    
    id_num_re = re.compile(u"身份证号</td><td colspan='2' >(.*?)<br>")
    name_re = re.compile(u"名</td><td colspan='2'>(.*?)<br>")
    academy_re = re.compile(u"部</td><td>(.*?)<br>")

    @classmethod
    def login(cls, url, stuid, password):
        encode = cls.md5(stuid + cls.md5(password)[:30].upper() + '10611')[:30].upper()
        res = requests.post(url + '/_data/index_login.aspx', data={
            '__VIEWSTATEGENERATOR': 'CAA0A5A7',
            'Sel_Type': 'STU',
            'txt_dsdsdsdjkjkjc': stuid,
            'efdfdfuuyyuuckjg': encode
        }, headers=cls.headers)
        if res.cookies.get('ASP.NET_SessionId'):
            cookie = res.cookies.get('ASP.NET_SessionId')
            cls.headers.update({'Cookie': 'ASP.NET_SessionId=' + cookie})
            res = requests.get(url + '/SYS/Main_banner.aspx', headers=cls.headers)
            if res.url.endswith('Main_banner.aspx'):
                return cookie
        return False

    @classmethod
    def get_stu_info(cls, stu_id, jwc_url, test_id, test_pass):
        """
        :param stu_id: 要查询的学号
        :param jwc_url: 教务处网址
        :param test_id: 自己的教务处账号
        :param test_pass: 自己的教务处账号密码
        :return: {'id_num': '', 'name': '', 'academy': ''}
        """
        cls.login(jwc_url, test_id, test_pass)
        r = requests.get(jwc_url + '/XSXJ/R_XJDA_CKXSDA_Detail.aspx?id=' + stu_id, headers=cls.headers)
        id_num = cls.id_num_re.search(r.text)
        name = cls.name_re.search(r.text)
        academy = cls.academy_re.search(r.text)
        if not (id_num and name and academy):
            return False
        return {'id_num': id_num.group(1), 'name': name.group(1), 'academy': academy.group(1)}

    @staticmethod
    def md5(str_):
        t = hashlib.md5()
        t.update(str_.encode('utf-8'))
        return t.hexdigest()


def get_stu_academy(stu_num):
    res = StuVerify.get_stu_info(stu_num, 'http://222.198.128.126', '20164404', '169197')
    return res['academy']


if __name__ == '__main__':
    print get_stu_academy('20164366')
