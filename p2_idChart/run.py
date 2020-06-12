from flask import Flask, request, jsonify,render_template
from config import FLASK_HOST,FLASK_PORT,\
    MYSQL_CLIENT,MYSQL_TABLE,ROOT_FIELD,\
    MONGO_COL,MONGO_DB,MONGO_HOST,MONGO_PORT
import json
import pymysql
from pymongo import MongoClient
import click  # 日志打印
import time

app = Flask(__name__)
MYSQL_CLIENT['cursorclass'] = pymysql.cursors.DictCursor

class mysql():
    def __init__(self):
        self.client = pymysql.connect(**MYSQL_CLIENT)
        self.cursor = self.client.cursor()
        self.table = MYSQL_TABLE

    def findall(self,parent_id):
        sql = 'SELECT * FROM {} WHERE parent_id={}'.format(self.table,repr(parent_id))
        self.cursor.execute(sql)
        # fetchone 返回元组
        result = self.cursor.fetchall()
        if result:
            return result
        return
    
    def findone(self,dir_name,parent_id):
        sql = 'SELECT * FROM {} WHERE dir_name={} AND parent_id={}'.format(self.table,repr(dir_name),repr(parent_id))
        self.cursor.execute(sql)
        # fetchone 返回元组
        result = self.cursor.fetchone()
        if result:
            return result
        return
    
    def close(self):
        self.client.close()


class mongo():
    def __init__(self):
        self.client = MongoClient(host=MONGO_HOST,port=MONGO_PORT)
        self.coll = self.client[MONGO_DB][MONGO_COL]
        
    def find(self,**kwargs):
        # 正常返回一个列表
        print("传递的参数为 {}".format(kwargs))
        try:
            datas = self.coll.find(kwargs)
            res = []
            for data in datas:
                data.pop('_id')
                res.append(data)
        except Exception as e:
            res = False
            print(e)
        return res
    
    def close(self):
        self.client.close()
        


@app.route('/', methods=['GET'])
def index():
    mysql_server = mysql()
    root_ret = mysql_server.findone(ROOT_FIELD['dir_name'],ROOT_FIELD['parent_id'])
    genertion_menu = mysql_server.findall(parent_id=ROOT_FIELD['id'])
    mysql_server.close()
    return render_template('index.html',root_name=root_ret['dir_name'],genertion_menu=genertion_menu)
    
@app.route('/get_genertion_menu', methods=['GET','POST'])
def get_genertion_menu():
    if request.method == 'POST':
        son_menu_id = request.form.get('son_menu_id',False)
        print("查询id为:{}".format(son_menu_id))
        mysql_server = mysql()
        son_menu = mysql_server.findall(parent_id=son_menu_id)
        mysql_server.close()
        return jsonify({"son_menu":son_menu})
    
@app.route('/show_data', methods=['GET','POST'])
def show_data():
    if request.method == 'POST':
        query_id = request.form.get('query_id',False)
        print("mongo查询id为:{}".format(query_id))
        mongo_server = mongo()
        datas = mongo_server.find(parent_id=query_id)
        # print(datas)
        data_x = []
        data_y = []
        for data in datas:
            data_x.append(data['create_time'])
            data_y.append(data['data_value'])
        mongo_server.close()
        return jsonify({"datas":{'data_x':data_x,'data_y':data_y}})

if __name__ == '__main__':
   app.run(host=FLASK_HOST,port=FLASK_PORT,debug = True)