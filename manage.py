from app import create_app,db,models
from flask_script import Manager,Shell

app=create_app()

manager=Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=models.User, Teacher=models.Teacher,CulProduct=models.CulProduct)
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def run():
    ''' run the app '''
    app.run(port=5000,host='0.0.0.0')

@manager.command
def refresh():
    '''db refresh'''
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()