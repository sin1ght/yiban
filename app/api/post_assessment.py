# coding=utf-8

import os
from . import api
from ..utils.success import success
from ..utils.error import error
from flask import session,request,current_app
from ..models import User,Assessment
from ..decorators import login_required
from ..utils.stu_verify import get_stu_academy
from datetime import datetime


@api.route('/post_assessment',methods=['GET','POST'])
@login_required
def post_assessment():
    if request.method=='POST':
        file=request.files['file']

        if not allowed_file(file.filename):
            return error('请上传合法的类型的文件')

        now_str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = now_str + file.filename

        userid=session['base_info']['userid']
        user=User.query.filter_by(id=userid).first()

        month=request.form.get('month',1)
        stu_num=request.form.get('stu_num','')
        s_academy=request.form.get('academy','')

        academy=None
        if get_stu_academy(stu_num) and len(stu_num)==8:
            academy=get_stu_academy(stu_num)
        else:
            return error('学号不符合规范')

        if academy!=s_academy:
            return error('学号与学院不符合')

        file_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER'), file_name)
        print file_dir
        file.save(file_dir)

        file_link=current_app.config.get('HOST')+'/upload/'+file_name
        print file_link
        comment=request.form.get('comment','')

        assessment=Assessment(file_name,month,academy,file_link,comment,user)
        assessment.save()

        return success({'msg':'上传成功','file_link':file_link})
    else:
        return error('请用post')


def allowed_file(filename):
    file_type=['doc','docx','pdf','xls','zip']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in file_type