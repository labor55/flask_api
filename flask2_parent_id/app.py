from flask import Flask, request, jsonify
from config import HOST, PORT
import json
import pymysql
import click  # 日志打印
import time

app = Flask(__name__)
'''
数据库字段设计
DROP TABLE  IF EXISTS parent;
CREATE TABLE IF NOT EXISTS parent (
  id BIGINT,
  dir_name VARCHAR (100),
  parent_id VARCHAR (30),
  level INT,
  PRIMARY KEY(id)
) ENGINE = INNODB DEFAULT CHARSET = UTF8;
实现功能：自动生成id表，
接收参数：POST请求，data:json.dump([])格式
返回参数：res:1  成功， res:0 失败
限制：数据库需要有一条主目录，
'''

config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'lab123456',
          'db':'test',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
client = pymysql.connect(**config)
cursor = client.cursor()

def select(cursor,dir_name,parent_id):
    sql = 'SELECT * FROM parent WHERE dir_name={} AND parent_id={}'.format(repr(dir_name),repr(parent_id))
    cursor.execute(sql)
    # fetchone 返回字典
    result = cursor.fetchone()
    if result:
        return result
    return

def insert(cursor,**dic):
    sql = 'INSERT INTO parent VALUES (%s,%s,%s,%s)'
    try:
        cursor.execute(sql,(dic['id'],dic['dir_name'],dic['parent_id'],dic['level']))
    except Exception as e:
        click.echo("插入操作异常，异常为{}".format(e))
        raise


def update(cursor,level,dir_name):
    sql = "UPDATE parent SET level=%s WHERE dir_name = %s"
    try:
        cursor.execute(sql,(level,dir_name))
    except Exception as e:
        click.echo("更新操作异常，异常为{}".format(e))
        raise

@app.route('/', methods=['GET'])
def index():
    return jsonify("(url='localhost:5001',data={'data:list'})")

@app.route('/get', methods=['POST'])
def get():
    pre_field = '石油和天然气开采业'
    pre_parent_id = '2002'
    if request.method == 'POST':
        data = request.form.get('data','')
        if data:
            jdata = json.loads(data)
            while jdata:
                # 获取当前列表的字段值
                cur_field = jdata.pop(0)
                # 查找数据库中是否有此字段
                cur_res = select(cursor,cur_field,pre_parent_id)
                # 如果有此字段
                if cur_res:
                    # 把此字段作为当前级别
                    click.echo('此字段存在:{}'.format(cur_res))
                    pre_field = cur_res['dir_name']
                    pre_parent_id = str(cur_res['id'])
                else:
                    # 查找上一级字段并进行更新
                    pre_res = select(cursor,pre_field,pre_parent_id[:-3])
                    click.echo('上一级的字段:{}'.format(pre_res))
                    time.sleep(1)
                    level = pre_res['level'] + 1
                    # updata和insert要同时生效
                    update(cursor,level,pre_field)
                    # 插入此字段
                    cur_col = pre_res
                    cur_col['id'] = int(str(pre_res['id']) + '0'*(3-len(str(level)))+str(level))
                    cur_col['dir_name'] = cur_field
                    cur_col['parent_id'] = str(cur_col['id'])[:-3]
                    cur_col['level'] = 0
                    click.echo('本级的字段:{}'.format(cur_col))
                    insert(cursor,**cur_col)
                    client.commit()
                    click.echo("更新成功")
                    pre_field = cur_field  # qwer
                    pre_parent_id = str(cur_col['id']) # 2002002
            return jsonify({'res':1})
        return jsonify({'res':0})

if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug = True)
