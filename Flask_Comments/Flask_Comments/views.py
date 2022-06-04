from datetime import datetime
from flask import render_template, request, redirect, url_for
from Flask_Comments import app
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from Flask_Comments.DB_Utils import DB
import os
import jieba
import collections
from Flask_Comments.page_utils import Pagination
import pandas as pd  # 数据分析包
import matplotlib.pyplot as plt
from PIL import Image
import wordcloud
import numpy as np  # numpy数据处理库


class MySQLConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{ipaddress}:{port}/{database}".format(username="root",
                                                                                                   password="root",
                                                                                                   ipaddress="127.0.0.1",
                                                                                                   port="3306",
                                                                                                   database="pl")
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 动态追踪修改设置
    SQLALCHEMY_ECHO = True
    JSON_AS_ASCII = False


app.config.from_object(MySQLConfig)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    sex = db.Column(db.String(1))
    password = db.Column(db.String(256))
    join_time = db.Column(db.DateTime)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    catename = db.Column(db.String(128))

    # id	comname


class Commodity(db.Model):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True)
    comname = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


# id	content	create_time	author_id	commodity_id
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    commodity_id = db.Column(db.Integer, db.ForeignKey("commodity.id"))


@app.route('/getCommentCount')
def getCommentCount():
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query(
        "SELECT catename 分类,COUNT(*) 评论数 FROM QUESTION INNER JOIN commodity ON question.commodity_id=commodity.ID INNER JOIN category ON commodity.category_id=category.id GROUP BY catename;")
    return jsonify(result)


@app.route('/getUserCount')
def getUserCount():
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query("SELECT CASE SEX WHEN '0' THEN '女' ELSE '男' END 性别,COUNT(*) 人数 FROM USER GROUP BY SEX ;")
    return jsonify(result)


@app.route('/')
@app.route('/home')
def home():
    # data = Question.query().filter()
    # print(data)
    # result = {'id': data.id, 'comname': data.comname}
    # return jsonify(data=result)

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
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
    )


@app.route('/user/<string:username>')
def user_by_key(username):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    if username:
        query_str = "SELECT USERNAME,EMAIL,SEX,JOIN_TIME,ID from user WHERE USERNAME LIKE '%{}%' ORDER BY JOIN_TIME DESC;".format(
            username)
    else:
        query_str = 'SELECT USERNAME,EMAIL,SEX,JOIN_TIME,ID from user ORDER BY JOIN_TIME DESC;'
    result = db.query(query_str)
    li = []
    for item in result:
        sex = '男'
        if item[2] == 0:
            sex = '女'
        u = {'username': item[0], 'email': item[1], 'sex': sex, 'join_time': item[3], 'id': item[4]}
        li.append(u)

    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("user.html", index_list=index_list, html=html)


@app.route('/user')
def user():
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = 'SELECT USERNAME,EMAIL,SEX,JOIN_TIME,ID from user ORDER BY JOIN_TIME DESC;'
    result = db.query(query_str)
    li = []
    for item in result:
        sex = '男'
        if item[2] == '0':
            sex = '女'
        u = {'username': item[0], 'email': item[1], 'sex': sex, 'join_time': item[3], 'id': item[4]}
        li.append(u)

    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("user.html", index_list=index_list, html=html)


@app.route('/comment')
def comment():
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = 'SELECT commodity.comname,question.content,USER.username,question.create_time,question.id from question INNER JOIN user ON question.author_id=USER.ID INNER JOIN COMMODITY ON question.commodity_id=commodity.ID;'
    result = db.query(query_str)
    li = []
    for item in result:
        u = {'comname': item[0], 'content': item[1], 'username': item[2], 'create_time': item[3], 'id': item[4]}
        li.append(u)

    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template("comment.html", index_list=index_list, html=html, comid='')


@app.route('/cipin/<string:category_name>')
def cipin(category_name):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query(
        "SELECT content from question where commodity_id in (select id from commodity where category_id = (select id from category where catename = '{}'));".format(
            category_name))
    list = []
    for item in result:
        list.append(item[0])
    str = ''.join(list)
    words = jieba.cut(str)
    stwlist = []
    for word in open('stopword.txt', 'r', encoding='utf-8'):
        stwlist.append(word.strip())

    word_ = {}
    for word in words:
        if word.strip() not in stwlist:
            if len(word) > 1:
                if word != '\t':
                    if word != '\r\n':
                        # 计算词频
                        if word in word_:
                            word_[word] += 1
                        else:
                            word_[word] = 1

    # 将词汇和词频以元组的形式保存
    word_freq = []
    for word, freq in word_.items():
        word_freq.append((word, freq))

    # 进行降序排列
    word_freq.sort(key=lambda x: x[1], reverse=True)

    ##查看前200个结果
    # for i in range(200):
    #    word,freq =word_freq[i]
    #    print('{0:10}{1:5}'.format(word,freq))

    most_10 = word_freq[:10]
    print(most_10)
    word_list = []
    cnt_list = []
    statistics_list = []
    num = 0
    for item in most_10:
        num += 1
        word_list.append(item[0])
        cnt_list.append(item[1])
        statistics_list.append([num, item[0], item[1]])
    return jsonify({'word_list': word_list, 'cnt_list': cnt_list, 'statistics_list': statistics_list})


@app.route('/getUserInfo/<int:id>')
def getUserInfo(id):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query(
        "SELECT USERNAME,EMAIL,SEX,DATE_FORMAT(JOIN_TIME,'%Y-%m-%d') JOIN_TIME,ID from user WHERE id={}".format(id))
    u = {'username': result[0][0], 'email': result[0][1], 'sex': result[0][2], 'join_time': result[0][3],
         'id': result[0][4]}
    return jsonify(u)


@app.route('/user_update', methods=['POST'])
def user_update():
    username = request.form.get('update_username')
    email = request.form.get('update_email')
    sex = request.form.get('update_sex')
    join_time = request.form.get('update_join_time')
    id = request.form.get('update_id')
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = "update user set USERNAME='{}',EMAIL='{}',SEX='{}',JOIN_TIME='{}' WHERE id={};".format(username, email,
                                                                                                       sex, join_time,
                                                                                                       id)
    print(query_str)
    db.update(query_str, False)
    return redirect(url_for('user'))


@app.route('/user_del/<int:id>')
def user_del(id):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = "delete from user WHERE id={};".format(id)
    print(query_str)
    db.update(query_str, True)
    return redirect(url_for('user'))


@app.route('/comment_del/<int:id>')
def comment_del(id):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = "delete from question WHERE id={};".format(id)
    print(query_str)
    db.update(query_str, True)
    return redirect(url_for('comment'))


@app.route('/commodity')
def getCommodity():
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = "select commodity.comname,category.catename,commodity.id from commodity inner join category on commodity.category_id=category.id;"
    result = db.query(query_str)
    list = []
    for item in result:
        u = {'comname': item[0], 'catename': item[1], 'id': item[2]}
        list.append(u)
    return jsonify(list)


@app.route('/comment/<int:commodityId>')
def getcommentByCommodityId(commodityId):
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    query_str = 'SELECT commodity.comname,question.content,USER.username,question.create_time,question.id from question INNER JOIN user ON question.author_id=USER.ID INNER JOIN COMMODITY ON question.commodity_id=commodity.ID where commodity.id={};'.format(
        commodityId)
    result = db.query(query_str)
    li = []
    for item in result:
        u = {'comname': item[0], 'content': item[1], 'username': item[2], 'create_time': item[3], 'id': item[4]}
        li.append(u)

    pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    print(commodityId)
    return render_template("comment.html", index_list=index_list, html=html, comid=str(commodityId))


@app.route('/commentVisualization')
def commentVisualization():
    return render_template(
        'commentVisualization.html',
        title='评论可视化',
        year=datetime.now().year,
    )


# @app.route('/')
@app.route('/userPortrait')
def userPortrait():
    return render_template(
        'userPortrait.html',
        title='用户画像',
        year=datetime.now().year,
    )


@app.route('/generateWordCloud', methods=['POST'])
def generateWordCloud():
    commodityId = request.form.get('commodityId')
    sw_str = request.form.get('sw_str')
    print(commodityId, sw_str)
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query("SELECT content from question where commodity_id = {};".format(commodityId))
    list = []
    for item in result:
        list.append(item[0])
    str = ''.join(list)

    segment = []
    segs = jieba.cut(str)  # 使用jieba分词进行切词
    sw_list = sw_str.split('，')

    # 将每个词根据补充停用词先进行一次过滤
    for seg in segs:
        if len(seg) > 1 and seg != '\r\n':
            if seg not in sw_list:
                segment.append(seg)

    # 去停用词
    words_df = pd.DataFrame({'segment': segment})
    words_df.head()
    stopwords = pd.read_csv("stopword.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding="utf-8")
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    # words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    # words_stat=words_stat.reset_index().sort_values(by="计数",ascending=False)
    # words_stat  #打印统计结果

    # 词频统计
    word_counts = collections.Counter(words_df['segment'])  # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(30)  # 获取前10最高频的词
    print(word_counts_top10)  # 输出检查

    # 增加高频词数量显示
    x = []
    y = []
    for item in word_counts_top10:
        x.append(item[0])
        y.append(item[1])

    # plt.bar(x, y, align='center',color='g') # 画图，设置x，y轴的数据
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # for x, y in zip(x, y):
    #    plt.text(x, y+0.05, '%.0f'%y, ha='center', va='bottom')
    # plt.xticks(rotation =90)# rotation设置x轴标签的旋转度数
    # plt.title('高频词柱形图统计评论')
    # plt.show()

    # 词频展示
    mask = np.array(Image.open('bk.jpg'))  # 定义词频背景
    wc = wordcloud.WordCloud(
        scale=4,
        font_path='static/fonts/simsun.ttc',  # 设置字体格式
        mask=mask,  # 设置背景图
        max_words=100,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )

    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    # plt.show() # 显示图像
    path = os.getcwd() + '\\Flask_Comments\\static\\'
    plt.savefig(path + 'wordcloud.png')

    return jsonify({'result': True})


@app.route('/generateCiPin', methods=['POST'])
def generateCiPin():
    commodityId = request.form.get('commodityId')
    sw_str = request.form.get('sw_str')
    sw_list = sw_str.split('，')

    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query("SELECT content from question where commodity_id = {};".format(commodityId))
    list = []
    for item in result:
        list.append(item[0])
    str = ''.join(list)
    words = jieba.cut(str)
    stwlist = []
    for word in open('stopword.txt', 'r', encoding='utf-8'):
        stwlist.append(word.strip())

    word_ = {}
    for word in words:
        if word.strip() not in sw_list:
            if word.strip() not in stwlist:
                if len(word) > 1:
                    if word != '\t':
                        if word != '\r\n':
                            # 计算词频
                            if word in word_:
                                word_[word] += 1
                            else:
                                word_[word] = 1

    # 将词汇和词频以元组的形式保存
    word_freq = []
    for word, freq in word_.items():
        word_freq.append((word, freq))

    # 进行降序排列
    word_freq.sort(key=lambda x: x[1], reverse=True)

    ##查看前200个结果
    # for i in range(200):
    #    word,freq =word_freq[i]
    #    print('{0:10}{1:5}'.format(word,freq))

    most_10 = word_freq[:10]
    print(most_10)
    word_list = []
    cnt_list = []
    statistics_list = []
    num = 0
    for item in most_10:
        num += 1
        word_list.append(item[0])
        cnt_list.append(item[1])
        statistics_list.append([num, item[0], item[1]])
    return jsonify({'word_list': word_list, 'cnt_list': cnt_list})


# @app.route('/')
@app.route('/generateUserPortrait', methods=['POST'])
def generateUserPortrait():
    commodityId = request.form.get('commodityId')
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query(
        "SELECT case sex when '0' then '女性' else '男性' end sex,count(sex) cnt from question inner join user on question.author_id=user.id where commodity_id={} group by sex;".format(
            commodityId))
    li = []
    for item in result:
        if item[0] == '女性':
            li.append({'value': item[1], 'name': item[0], 'itemStyle': {'color': '#fc8251'}})
        else:
            li.append({'value': item[1], 'name': item[0], 'itemStyle': {'color': '#5470c6'}})

    print(li)
    return jsonify(li)


@app.route('/generateCommentsTimePortrait', methods=['POST'])
def generateCommentsTimePortrait():
    commodityId2 = request.form.get('commodityId2')
    db = DB('127.0.0.1', 3306, 'root', 'root', 'pl')
    result = db.query(
        "select date_format(create_time,'%Y-%m-%d') ft_date,count(*) cnt from question where commodity_id={} group by date_format(create_time,'%Y-%m-%d') order by ft_date;".format(
            commodityId2))
    x = []
    y = []
    for item in result:
        x.append(item[0])
        y.append(item[1])
    d = {'x': x, 'y': y}
    return jsonify(d)
