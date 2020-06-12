from flask import Flask, request, jsonify
from config import HOST, PORT,MYSQL_CLIENT,MYSQL_TABLE,\
    ROOT_FIELD
import json
import pymysql
import click  # 日志打印
import time

app = Flask(__name__)
MYSQL_CLIENT['cursorclass'] = pymysql.cursors.DictCursor

class mysql():
    def __init__(self):
        self.client = pymysql.connect(**MYSQL_CLIENT)
        self.cursor = self.client.cursor()
        self.table = MYSQL_TABLE

    def select(self,dir_name,parent_id):
        sql = 'SELECT * FROM {} WHERE dir_name={} AND parent_id={}'.format(self.table,repr(dir_name),repr(parent_id))
        self.cursor.execute(sql)
        # fetchone 返回字典
        result = self.cursor.fetchone()
        if result:
            return result
        return
    def insert(self,**dic):
        sql = 'INSERT INTO {} VALUES ({},{},{},{})'.format(self.table,repr(dic['id']),repr(dic['dir_name']),repr(dic['parent_id']),repr(dic['level']))
        try:
            self.cursor.execute(sql)
        except Exception as e:
            click.echo("插入操作异常，异常为:{}".format(e))
            with open('error.log','a',encoding='utf8') as f:
                f.write('插入异常字段为:' + dic['dir_name'] +'\n')
    def update(self,level,dir_name):
        sql = "UPDATE {} SET level={} WHERE dir_name = {}".format(self.table,repr(level),repr(dir_name))
        try:
            self.cursor.execute(sql,)
        except Exception as e:
            click.echo("更新操作异常，异常为:{}".format(e))
            with open('error.log','a',encoding='utf8') as f:
                f.write('更新异常字段为:' + dir_name +'\n')

@app.route('/', methods=['GET'])
def index():
    return jsonify("url='http://{}:{}',data={'data:list'}".format(HOST,PORT))

@app.route('/get', methods=['POST'])
def get():
    pre_field = ROOT_FIELD['dir_name']
    pre_pid = str(ROOT_FIELD['id'])
    if request.method == 'POST':
        data = request.form.get('data','')
        if data:
            jdata = json.loads(data)
            while jdata:
                # 获取当前列表的字段值
                cur_field = jdata.pop(0)
                # 查找数据库中是否有此字段
                cur_res = client.select(cur_field,pre_pid)
                # 如果有此字段
                if cur_res:
                    # 把此字段作为当前级别
                    pre_field = cur_res['dir_name']
                    pre_pid = str(cur_res['id'])
                else:
                    # 查找上一级字段并进行更新
                    pre_res = client.select(pre_field,pre_pid[:-3])
                    level = pre_res['level'] + 1
                    # updata和insert要同时生效
                    client.update(level,pre_field)
                    # 插入此字段
                    cur_col = pre_res
                    cur_col['id'] = int(str(pre_res['id']) + '0'*(3-len(str(level)))+str(level))
                    cur_col['dir_name'] = cur_field
                    cur_col['parent_id'] = str(cur_col['id'])[:-3]
                    cur_col['level'] = 0
                    client.insert(**cur_col)
                    client.client.commit()
                    click.echo("更新成功")
                    pre_field = cur_field
                    pre_pid = str(cur_col['id'])
                    time.sleep(0.5)
            return jsonify({'res':pre_pid})
        return jsonify({'res':0})

if __name__ == '__main__':
    # 全局变量
    client = mysql()
    # 插入第一条，确保数据库中至少有根目录
    first_root = client.select(ROOT_FIELD['dir_name'],(ROOT_FIELD['parent_id']))
    if not first_root:
        click.echo('插入根目录:{}'.format(ROOT_FIELD))
        client.insert(**ROOT_FIELD)
        client.client.commit()
    else:
        click.echo('存在根目录{}'.format(first_root))
    app.run(host=HOST,port=PORT,debug = True)
