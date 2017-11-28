# coding=utf-8
from app import db
import datetime


class Teacher(db.Model):
    id=db.Column(db.String(10),primary_key=True,doc="用户易班id")
    academy=db.Column(db.String(15), doc="用户所在学院")
    status = db.Column(db.Integer, default=0,nullable=True, doc="用户身份类型:0 is 学生，1 is 院易班指导老师 2 is 校易班指导老师")

    def __init__(self, id, academy, status):
        self.status=status
        self.id=id
        self.academy=academy

    def __repr__(self):
        return '<User %s,%s>' % (self.id, self.academy)

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    id = db.Column(db.String(10), primary_key=True, doc="用户易班id")
    sex = db.Column(db.String(4), doc="用户性别:M 男，W 女")
    nick = db.Column(db.String(80), doc="用户易班昵称")
    head_img = db.Column(db.String(255), doc="用户头像链接")
    #name = db.Column(db.String(80), doc="用户真实姓名")
    stu_num = db.Column(db.String(12), nullable=True,doc="用户学号")
    academy = db.Column(db.String(15), doc="用户所在学院", nullable=True)
    status = db.Column(db.Integer, default=0,nullable=True, doc="用户身份类型:0 is 学生，1 is 院易班指导老师 2 is 校易班指导老师")
    #create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, id, sex, nick, head_img,stu_num,academy,status):
        self.id = id
        self.sex=sex
        self.nick=nick
        self.head_img=head_img
        self.stu_num=stu_num
        self.academy=academy
        self.status=status

    def to_json(self):
        return {
            'id':self.id,
            'sex':self.sex,
            'nick':self.nick,
            'head_img':self.head_img,
            'status':self.status,
            'academy':self.academy
        }

    def __repr__(self):
        return '<User %s,%s %s>' % (self.id, self.nick, self.academy)

    def save(self):
        db.session.add(self)
        db.session.commit()


class BaseSubmit(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    academy = db.Column(db.String(15), default='', doc="所属学院")
    progress = db.Column(db.Integer, default=0, doc="审核进程 0 is 等待审核，1 is 第一步审核完成,类推")
    verify_res = db.Column(db.Integer, default=0, doc="阶段审核状态 0 is 等待审核，1 is 审核驳回 2 审核通过")
    create_time = db.Column(db.String(20), default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), doc="提交日期")
    reason = db.Column(db.Text, default='', doc="审核驳回的说明（后台加入处理人信息）")

    def __init__(self,academy):
        self.academy=academy
        self.create_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self,progress=None,verify_res=None,reason=''):
        if progress:
            self.progress=progress
        if verify_res:
            self.verify_res=verify_res
        self.reason=reason

        db.session.commit()


class Assessment(BaseSubmit,db.Model):
    """学院月度考核"""
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # academy = db.Column(db.String(15), default='', doc="所属学院")
    # progress = db.Column(db.Integer, default=0, doc="审核进程 0 is 等待审核，1 is 第一步审核完成,类推")
    # verify_res = db.Column(db.Integer, default=0, doc="阶段审核状态 0 is 等待审核，1 is 审核驳回 2 审核通过")
    # create_time = db.Column(db.DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), doc="提交日期")
    # reason = db.Column(db.Text, default='', doc="审核驳回的说明（后台加入处理人信息）")

    name=db.Column(db.String(40),doc='文件名称')
    month = db.Column(db.Integer, doc="考核月份，1 is 一月，类推")
    file_link = db.Column(db.Text, doc="附件链接")
    comment = db.Column(db.Text, doc="备注")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), doc="提交者易班id")
    user = db.relationship('User', backref=db.backref('assessments', lazy='dynamic'),doc='提交者')

    def __init__(self, name,month, academy,file_link,comment,user):
        super(Assessment, self).__init__(academy)
        self.name=name
        self.month=month
        # self.academy=academy
        self.file_link=file_link
        self.comment=comment
        self.user=user

    def to_json(self):
        return {
            'name':self.name,
            'month':self.month,
            'academy':self.academy,
            'progress':self.progress,
            'file_link':self.file_link,
            'comment':self.comment,
            'verify_res':self.verify_res,
            'reason':self.reason,
            'create_time':self.create_time,
            'flag': str(self.user_id) + '#' + self.create_time  # 唯一标识  提交者易班id+提交时间组成
        }

    def __repr__(self):
        return '<Assessment %s学院,%s月 考核>' % (self.academy, self.month)

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
    #
    # def update(self,progress=None,verify_res=None,reason=''):
    #     if progress:
    #         self.progress=progress
    #     if verify_res:
    #         self.verify_res=verify_res
    #     self.reason=reason
    #
    #     db.session.commit()


class CulProduct(BaseSubmit,db.Model):
    """文化产品"""

    name=db.Column(db.String(40),doc='产品名称')
    category=db.Column(db.String(20),doc='类别')
    num=db.Column(db.Integer,doc='数量')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), doc="提交者易班id")
    user = db.relationship('User', backref=db.backref('culproducts', lazy='dynamic'), doc='提交者')

    def __init__(self,academy,name,category,num,user):
        super(CulProduct, self).__init__(academy)
        self.name=name
        self.category=category
        self.num=num
        self.user=user

    def to_json(self):
        return {
            'name': self.name,
            'category':self.category,
            'num':self.num,
            'academy': self.academy,
            'progress': self.progress,
            'verify_res': self.verify_res,
            'reason': self.reason,
            'create_time': self.create_time,
            'flag':str(self.user_id)+'#'+self.create_time  #唯一标识  提交者易班id+提交时间组成
        }

    def __repr__(self):
        return '<CulProduct %s,%s>' % (self.academy, self.name)


class Good(BaseSubmit,db.Model):
    """物资申请"""
    name = db.Column(db.String(40), doc='产品名称')
    category = db.Column(db.String(20), doc='类别')
    num = db.Column(db.Integer, doc='数量')
    last_time=db.Column(db.String(10),doc='借用时长')

    is_lendOrReturn=db.Column(db.Integer,default=0,doc='0 审核中 1 已借出 2已归还')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), doc="提交者易班id")
    user = db.relationship('User', backref=db.backref('goods', lazy='dynamic'), doc='提交者')

    def __init__(self, academy, name, category, num,last_time, user):
        super(Good, self).__init__(academy)
        self.name=name
        self.category=category
        self.num=num
        self.last_time=last_time
        self.user=user

    def __repr__(self):
        return '<Good %s,%s>' % (self.academy, self.name)

    def to_json(self):
        return {
            'name':self.name,
            'category':self.category,
            'num':self.num,
            'last_time':self.last_time,
            'is_lendOrReturn':self.is_lendOrReturn,
            'academy': self.academy,
            'progress': self.progress,
            'verify_res': self.verify_res,
            'reason': self.reason,
            'create_time': self.create_time,
            'flag': str(self.user_id) + '#' + self.create_time  # 唯一标识  提交者易班id+提交时间组成
        }

    def update(self,progress=None,verify_res=None,reason='',is_lend_return=None):
        if progress:
            self.progress=progress
        if verify_res:
            self.verify_res=verify_res
        self.reason=reason
        if is_lend_return:
            self.is_lendOrReturn=is_lend_return

        db.session.commit()
