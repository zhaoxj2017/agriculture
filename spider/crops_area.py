import lxml.html as H
import requests
from db.DBUtils import *
import json

session = requests.Session()
session.cookies['__cfduid'] = 'd9cd2186347d262c5799db11bf31669ce1525154073'
session.cookies['cf_clearance'] = '0da5e18b6f1bc9a770b61febd82f1569d417f539-1525154077-31536000'
headers = {
    "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36''',
    "Accept": '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'''}


def get_response(url):
    response = session.get(url, headers=headers)
    response.encoding = 'utf8'
    return response


def get_document(url):
    res = get_response(url)
    document = H.document_fromstring(res.text)
    return document


def get_json(url):
    res = get_response(url)
    json_data = json.loads(res.text, encoding="utf8")
    return json_data


def get_url(provence_id: str, index: int, market_id: int):
    return 'http://www.vegnet.com.cn/Price/List_ar' + provence_id + '_p' + str(index) + '.html?marketID=' + str(market_id)


def read_page(provence_id, market_id):
    pages_index = 1
    flag = True
    while flag:
        url = get_url(provence_id, pages_index, market_id)
        document = get_document(url)
        rows_len = get_rows_len(document)
        rows = read_rows(document, rows_len)
        store_into_mysql(rows)
        flag = is_last_page(document)
        pages_index += 1


def is_last_page(document):
    mark = len(document.xpath("/html/body/div/div[2]/div[2]/div[2]/text()")) - 1
    try:
        document.xpath('/html/body/div/div[2]/div[2]/div[2]/a[' + str(mark) + ']/text()')[0]
    except:
        print("Worn: at the end of pages")
        return False
    else:
        return True


def get_rows_len(document):
    return len(document.xpath('/html/body/div/div[2]/div[2]/div[1]/p'))


def read_rows(document, rows_len=0):
    rows = []
    for i in range(1, rows_len):
        row = dict(
            date_time=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[1]/text()')[0],
            varieties=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[2]/text()')[0],
            area=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[3]/a/text()')[0],
            low_price=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[4]/text()')[0],
            high_price=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[5]/text()')[0],
            avg_price=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[6]/text()')[0],
            mea_unit=document.xpath('/html/body/div/div[2]/div[2]/div[1]/p[' + str(i) + ']/span[7]/text()')[0])
        rows.append(row)
    return rows


# store into MySQL
def store_into_mysql(rows: list):
    conn = get_instance()
    cursor = conn.cursor()
    for row in rows:
        cursor.execute('''insert into crops_area(varieties,\
        area,low_price,high_price,avg_price,mea_unit,date_time) values(\
        "%s","%s","%s","%s","%s","%s","%s")''' % (row.get("varieties"), row.get("area"),
                                                  row.get("low_price"), row.get("high_price"), row.get("avg_price"),
                                                  row.get("mea_unit"), row.get("date_time")))
    conn.commit()


#######################################################################################################################
# read market
#######################################################################################################################

def get_province():
    url = 'http://www.vegnet.com.cn/Price/'
    document = get_document(url)
    province = document.xpath('//*[@id="selectArea"]/option[2]/text()')[0]
    province_tols = len(document.xpath('//*[@id="selectArea"]')[0])
    pro_info = {}
    i = 2
    while i <= province_tols:
        pro_info[document.xpath('//*[@id="selectArea"]/option[' + str(i) + ']/text()')[0]] = \
            document.xpath('//*[@id="selectArea"]/option[' + str(i) + ']/@value')[0]
        i += 1
    return pro_info


def get_market_url(area_id):
    return 'http://www.vegnet.com.cn/Market/GetMarketByAreaID?areaID=' + area_id


# get Guangdong provence information
def get_info():
    pro_info = get_province()
    url = get_market_url(pro_info["广东省"])
    json_data = get_json(url)
    markets = []
    for record in json_data:
        market = {"MarketID": record["MarketID"],
                  "Name": record["Name"]}
        markets.append(market)
    for index in markets:
        read_page(pro_info["广东省"], index["MarketID"])

if __name__ == '__main__':
    pass