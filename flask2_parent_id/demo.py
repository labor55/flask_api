import requests
import json
url = "http://localhost:5001/get"
datas = [
    {'data':json.dumps(['qewr','123','qwe','wera'])},
    {'data':json.dumps(['qewr','321','qwe','wera'])},
    {'data':json.dumps(['qewr','123','xcbv','wera'])},
    {'data':json.dumps(['123','123','qwe','wera'])},
]
for data in datas:
    res = requests.post(url, data=data)
jres = json.loads(res.text)['res']

print(jres)
