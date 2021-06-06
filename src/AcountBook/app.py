from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/accountbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

#创建模型
class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.String(18),primary_key=True)
    password=db.Column(db.String(18),unique=True)
    accounts=db.relationship('Account',backref='user')

class Account(db.Model):
    __tablename__='acoount'
    id=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date)
    type=db.Column(db.String(5))
    menoy=db.Column(db.Float)
    fk_user_id=db.Column(db.String(18),db.ForeignKey('user.user_id'))




@app.route('/',methods=['POST','GET'])
def Login():
    if request.method=='GET':
        return render_template('login.html',label='')
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(user_id=username).first()
        users=User.query.all()
        for a in users:
            print(a.user_id)
        if user:
            if user.password==password:
                #重定向了
                return url_for('/interface/'+username)
            else:
                return render_template('login.html',label='账号密码错误')
        else:
            return render_template('login.html',label='账号密码错误')


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='GET':
        return render_template('register.html',label='')
    else:
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(user_id=username)
        if username=='' or password=='':
            return render_template('register.html',label='输入不能为空')
        elif len(username)>18 or len(password)>18:
            return render_template('register.html',label='输出超过最大长度')
        elif user:
            return render_template('register.html',label='已存在相同用户名')
        else:
            new_add_user=User(user_id=username,password=password)
            db.session.add(new_add_user)
            db.session.commit()
            return render_template('register.html',label='注册成功')


@app.route('/interface/<user_id>',methods=['POST'])
def interface(user_id):
    pass


# db.create_all()

if __name__ == '__main__':
    app.run()
