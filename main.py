from spider.basic_crops import post_and_store
from db.tables import create_tables
from spider.crops_area import read_page
from spider.crops_area import get_info
# from spider.district import get_years_list
from spider.district import request_and_store
from spider.district import store_into_file

# create table into mysql to store web data
# create_tables()

# request from http://www.cgris.net/query/o.php
post_and_store()

# request from http://www.vegnet.com.cn
# get_info()


# request from http://www.xzqh.org/html/list/21.html
# get_years_list()
# request_and_store(datetime='2005')
# store_into_file("test")



