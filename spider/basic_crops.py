# -*- coding: utf-8 -*-，
# coding = utf-8

# 爬取中国种质网站 http://www.cgris.net/

import requests
import json
from db.DBUtils import *

url = 'http://www.cgris.net/query/o.php'
parameter = {"action": "menu"}


# 请求数据
def post_data():
    wb_data = requests.post(url, parameter)
    wb_data.encoding = 'utf8'
    # store into file
    store_into_file(wb_data.text)
    # change data format
    json_data = json.loads(wb_data.text, encoding="utf8")
    return json_data


def store_into_mysql(rows):
    conn = get_instance()
    cursor = conn.cursor()
    for row in rows:
        cursor.execute("insert into crops(vegetables) values('%s')" % row)
    conn.commit()
    cursor.execute("select * from crops")
    data = cursor.fetchall()
    print(data)


def store_into_file(content: str):
    file = open("sourcefile/crops/crops.html", "w")
    file.write(content)
    file.close()


# 解析json数据
def parse(json_data):
    rows = list()
    i = 0
    while i < len(json_data):
        rows.append(json_data[i][0])
        i += 1
    return rows


# 请求并存储
def post_and_store():
    json_data = post_data()
    rows = parse(json_data)
    store_into_mysql(rows)
