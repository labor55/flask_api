# 服务器配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

# mysql 配置
MYSQL_CLIENT = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'。。。。。',
    'db':'industry',
    'charset':'utf8mb4',
}

MYSQL_TABLE = '。。。。。'

# root 根目录配置
ROOT_FIELD = {
    'dir_name' : '能源',
    'id' : 7,
    'parent_id' : '0',
    'level' : 0,
}

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'RESOURCES'
MONGO_COL = 'data'
