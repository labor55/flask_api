import requests
import json
import time
import copy

ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100Safari/537.36'

class Iimei():
    def __init__(self):
        self.headers = {
                'Host': 'data.iimedia.cn',
                'Origin': 'https://data.iimedia.cn',
                'Referer': 'https://data.iimedia.cn/page-category.jsp?nodeid= 13669018',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': ua
            }
        self.url = 'https://data.iimedia.cn/front/search'
        self.data = {
            'nodeIdOfRoot': '71115',
            'key': '石油',
            'sourceType': '1',
            'returnType': '0',
        }
    def get_nodes(self):
        res = requests.post(self.url,headers=self.headers,data = self.data)
        jres = json.loads(res.text)
        data_nodes = jres['data']['index']
        return data_nodes

    def get_data_id(self, data_nodes,path=None):
        if path == None:
            path = []
        all = []
        for da in data_nodes:
            name = da['name']
            child = da['child']
            path.append(name)
            if child:
                all_ = self.get_data_id(child, path)
                all.extend(all_)  # 在列表末尾追加可迭代对象中的元素
            else:
                ids = da['childIds']  # 层级的ID
                p = copy.deepcopy(path)  # 层级目录列表（除最后一级）
                all.append((ids, p))
            path.pop(-1)
        return all


def pid_api(data_list):
    p_data = {'data':json.dumps(data_list)}
    url = "http://localhost:5020/get"
    p_res = requests.post(url, data=p_data)
    pid = json.loads(p_res.text)['res']
    print(pid)
    time.sleep(1)

Imer = Iimei()
data_nodes = Imer.get_nodes()
res = Imer.get_data_id(data_nodes)

for i in res:
    indics = i[1][-3:]  # 目录列表
    if indics:
        # print(indics)
        pid_api(indics)
