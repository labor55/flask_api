
def value_to_key(q_dict,query_val):
    if query_val in q_dict.values():
        res =  list(q_dict.keys())[list(q_dict.values()).index(query_val)]
        return res
    else:
        return

def client_mongo(host,port,db,coll):
    pass

if __name__ == '__main__':
    from config import COLUMN_CATE
    while True:
        get_value = input('请输入要查值：')
        if get_value == "q":
            break
        res = value_to_key(COLUMN_CATE,get_value)
        print(res)
