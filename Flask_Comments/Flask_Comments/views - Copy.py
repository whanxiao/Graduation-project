"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from Flask_Comments import app
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from Flask_Comments.DB_Utils import DB

import jieba
import collections

from flask import request
from Flask_Comments.page_utils import Pagination

class MySQLConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{ipaddress}:{port}/{database}".format(username="root", password="666666", ipaddress="127.0.0.1", port="3306", database="pl")
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 动态追踪修改设置
    SQLALCHEMY_ECHO = True
    JSON_AS_ASCII = False


app.config.from_object(MySQLConfig)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    sex = db.Column(db.String(1))
    password = db.Column(db.String(256))
    join_time = db.Column(db.DateTime)

class Category(db.Model):
    __tablename__='category'
    id = db.Column(db.Integer,primary_key=True)
    catename = db.Column(db.String(128))

    #id	comname
class Commodity(db.Model):
    __tablename__= 'commodity'
    id = db.Column(db.Integer,primary_key=True)
    comname = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

#id	content	create_time	author_id	commodity_id
class Question(db.Model):
    __tablename__= 'question'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    commodity_id = db.Column(db.Integer, db.ForeignKey("commodity.id"))


@app.route('/getCommentCount')
def getCommentCount():
    db = DB('127.0.0.1',3306,'root','666666','pl')
    result = db.query("SELECT catename 分类,COUNT(*) 评论数 FROM QUESTION INNER JOIN commodity ON question.commodity_id=commodity.ID INNER JOIN category ON commodity.category_id=category.id GROUP BY catename;")
    return jsonify(result)


@app.route('/getUserCount')
def getUserCount():
    db = DB('127.0.0.1',3306,'root','root','pl')
    result = db.query("SELECT CASE SEX WHEN '0' THEN '女' ELSE '男' END 性别,COUNT(*) 人数 FROM USER GROUP BY SEX ;")
    return jsonify(result)

@app.route('/')
@app.route('/home')
def home():
    #data = Question.query().filter()
    #print(data)
    #result = {'id': data.id, 'comname': data.comname}
    #return jsonify(data=result)




    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

#@app.route('/user')
#def user():
#    """Renders the user page."""

#    li = []
#    for i in range(1, 1000):
#        li.append(i)
#    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
#    print(request.path)
#    print(request.args)
#    index_list = li[pager_obj.start:pager_obj.end]
#    html = pager_obj.page_html()
#    return render_template("user.html",
#                           index_list=index_list,
#                           html=html,
#                           title='用户管理',
#                           year=datetime.now().year,
#                           )


#    #return render_template(
#    #    'user.html',
#    #    title='用户管理',
#    #    year=datetime.now().year,
#    #)


@app.route('/cipin/<string:category_name>')
def cipin(category_name):
    db = DB('127.0.0.1',3306,'root','root','pl')
    result = db.query("SELECT content from question where commodity_id in (select id from commodity where category_id = (select id from category where catename = '{}'));".format(category_name))
    list=[]
    for item in result:
        list.append(item[0])
    str = ''.join(list)
    words = jieba.cut(str)
    stwlist=[]
    for word in open('stopwords.txt','r'):
        stwlist.append(word.strip())


    word_ = {}
    for word in words:
        if word.strip() not in stwlist:
            if len(word) > 1:
                if word != '\t':
                    if word != '\r\n':
                        #计算词频
                        if word in word_:
                            word_[word] += 1
                        else:
                            word_[word] = 1

    #将词汇和词频以元组的形式保存
    word_freq = []
    for word,freq in word_.items():
        word_freq.append((word,freq))


    #进行降序排列
    word_freq.sort(key = lambda x:x[1],reverse = True)

    ##查看前200个结果
    #for i in range(200):
    #    word,freq =word_freq[i]
    #    print('{0:10}{1:5}'.format(word,freq))

    most_10 = word_freq[:10]
    print(most_10)
    word_list=[]
    cnt_list=[]
    statistics_list=[]
    num=0
    for item in most_10:
        num+=1
        word_list.append(item[0])
        cnt_list.append(item[1])
        statistics_list.append([num,item[0],item[1]])
    return jsonify({'word_list':word_list,'cnt_list':cnt_list,'statistics_list':statistics_list})