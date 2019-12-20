写这个接口的起因是艾媒数据库目录太多，看着着实令人绝望，故用flask写了一个生成parent_id接口，

**配置好config.py文件**

### 接口描述：

前提假设：有一个list类型的dir_name, 例如`['石油'，'石油价格'，'汽油具体价格']`

描述：

​	向此api发送**POST**请求，这样你数据库就会生成三条数据,并返回**石油具体价格**的parent_id，

​	所以你的spider.py中就可以这样

```python
	p_data = {'data':json.dumps(['石油'，'石油价格'，'汽油具体价格'])}
    url = "http://localhost:5020/get"
    p_res = requests.post(url, data=p_data)
    pid = json.loads(p_res.text)['res']
    if pid:
    	item['parent_id']=pid
```

当然返回的格式是字符串格式，

**请求正常返回**: `{'res':parent_id}`

**请求失败返回**:  `{'res':0}`

mysql插入失败有error.log文件，可以定位错误，当然，错误了就会中断程序执行，因为程序依赖上一条插入值进行自动更新id的，下一次运行请清空此log文件。

目录很多的时候，插入失败有可能为连接数据库有问题或者查询时间不够，一般来说，**要设置延时**

### 参数设置

入口参数：`{"data":json.dumps([])}` 要用json.dumps格式化 你的目录列表

返回参数：res:1  成功， res:0 失败

实现功能：自动生成mysql 的id表，并返回最底层的parent_id

限制：数据库需要有一条主目录，在config.py中设置好



### mysql数据库字段设计

```mysql
CREATE TABLE IF NOT EXISTS parent (
  id BIGINT,
  dir_name VARCHAR (100),
  parent_id VARCHAR (30),
  level INT,
  PRIMARY KEY(id)
) ENGINE = INNODB DEFAULT CHARSET = UTF8;
```

**注意** 字段level为自动更新id的依据，其意义为记录该条数据有多少个子目录

### 最后
更新时间：2019-12-20
**不足之处还请提出来**
