# -*- coding: utf-8 -*-，
# coding = utf-8

import requests
import json
from db.DBUtils import *

url = 'http://www.cgris.net/query/o.php'
parameter = {"action": "menu"}


def post_data():
    wb_data = requests.post(url, parameter)
    wb_data.encoding = 'utf8'
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


def parse(json_data):
    rows = list()
    i = 0
    while i < len(json_data):
        rows.append(json_data[i][0])
        i += 1
    return rows


def post_and_store():
    json_data = post_data()
    rows = parse(json_data)
    store_into_mysql(rows)
