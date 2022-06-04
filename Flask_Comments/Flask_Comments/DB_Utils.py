# coding=utf-8
'''
封装的mysql常用函数
'''

import MySQLdb

class DB():

    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PWD, DB_NAME):

        self.DB_HOST = DB_HOST

        self.DB_PORT = DB_PORT

        self.DB_USER = DB_USER

        self.DB_PWD = DB_PWD

        self.DB_NAME = DB_NAME

        self.conn = self.getConnection()

    def getConnection(self):

        return MySQLdb.Connect(

        host=self.DB_HOST, #设置MYSQL地址

        port=self.DB_PORT, #设置端口号

        user=self.DB_USER, #设置用户名

        passwd=self.DB_PWD, #设置密码

        db=self.DB_NAME, #数据库名

        charset='utf8' #设置编码

        )

    def query(self, sqlString):

        cursor=self.conn.cursor()

        cursor.execute(sqlString)

        returnData=cursor.fetchall()

        cursor.close()

        self.conn.close()

        return returnData

    def update(self, sqlString,check_foreign_key):

        cursor=self.conn.cursor()
        if check_foreign_key==True:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')           
        cursor.execute(sqlString)
        if check_foreign_key==True:
            cursor.execute('SET FOREIGN_KEY_CHECKS=1;')
        self.conn.commit()

        cursor.close()

        self.conn.close()