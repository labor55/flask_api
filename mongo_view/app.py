from flask import Flask, request, redirect, url_for, \
    abort, render_template, jsonify
import pymongo
from config import COLUMN, HOST, PORT, COLUMN_DATA,COLUMN_CATE
import json
from fun_lib import value_to_key

client = None
client_db = None
client_coll = None
temp = {}

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

# 资讯类查询
@app.route('/detail_cate', methods=['GET','POST'])
def detail_cate():
    if request.method == 'POST':
        # 获取form表单提交的文本
        host = request.form.get('host',False)
        port = request.form.get('port',False)
        db = request.form.get('db',False)
        coll = request.form.get('coll',False)

        # 连接mongo数据库
        global client
        client = pymongo.MongoClient(host, int(port))
        global client_db
        client_db = client[db]
        global client_coll
        client_coll = client_db[coll]

        # 进行查询操作
        total_num = client_coll.count() # 数据库总数
        for col,name in COLUMN_CATE.items():
            # 查询每人对应的数量
            cate_num = client_coll.find({"industry_Lcategories":col}).count()
            temp[name] = cate_num
        # 返回  名字：数目
        return render_template('detail_cate.html', count = total_num,result=temp)

# 资讯类ajax 返回
@app.route('/cate_data', methods=['GET','POST'])
def cate_data():
    if request.method == 'POST':
        cate = request.form.get('cate',False)  # 名字
        print(cate)
        cate_key = value_to_key(COLUMN_CATE,cate) # 行业
        if cate_key:
            info_cate = {}
            for col in COLUMN:
                cres = client_coll.find({"industry_Lcategories":cate_key,"information_categories":col}).count()
                info_cate[col] = cres
            return jsonify({"cate_datas":info_cate})
        if cate == "全部":
            return jsonify({"cate_datas":temp})



# 数据类查询
@app.route('/detail_data', methods=['GET','POST'])
def detail_data():
    if request.method == 'POST':
        # 获取form表单提交的文本
        host = request.form.get('host',False)
        port = request.form.get('port',False)
        db = request.form.get('db',False)
        coll = request.form.get('coll',False)

        # 连接mongo数据库
        global client
        client = pymongo.MongoClient(host, int(port))
        global client_db
        client_db = client[db]
        global client_coll
        client_coll = client_db[coll]
        # 进行查询操作
        cates = {}  # 返回  名字：数目
        total_num = client_coll.count()  # 数据库总数
        for col,name in COLUMN_DATA.items():
            cate_num = client_coll.find({"sign":col}).count()  # 查询名字对应数量
            cates[name] = cate_num
        return render_template('detail_data.html', count = total_num,result=cates)


if __name__ == '__main__':
   app.run(host=HOST,port=PORT,debug = True)
