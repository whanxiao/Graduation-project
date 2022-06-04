from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    # now加括号是运行项目的当前时间，不加括号是调用函数时存储的时间
    create_time = db.Column(db.DateTime, default=datetime.now)

class CommodityModel(db.Model):
    __tablename__ = "commodity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comname = db.Column(db.String(200), nullable=False, unique=False)

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    sex = db.Column(db.SmallInteger, default=0)
    def set(self):
        if self.sex == 0:
            return '女'
        else:
            return '男'
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    commodity_id = db.Column(db.Integer, db.ForeignKey("commodity.id"))

    author = db.relationship("UserModel", backref="questions")
    commodity = db.relationship("CommodityModel", backref="questions")
