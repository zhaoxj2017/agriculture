from spider.basic_crops import post_and_store
from db.tables import create_tables
from spider.crops_area import read_page
from spider.crops_area import get_info

# create table into mysql to store web data
create_tables()

# request from http://www.cgris.net/query/o.php
# post_and_store()

# request from http://www.vegnet.com.cn
get_info()




