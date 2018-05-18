from db.DBUtils import *
import requests
import lxml.html as H
import re

# 爬取中国行政区域网

headers = {
    "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36''',
    "Accept": '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8''',
    "Accept-Encoding": "gzip, deflate"}


def get_info_url(href_):
    print("http://www.xzqh.org/html/" + href_)
    return "http://www.xzqh.org/html/" + href_


def get_response(url):
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    return res


def get_document(url, datetime="2016"):
    res = get_response(url)
    store_into_file(res.text, datetime)
    return H.document_fromstring(res.text)


#######################################################################################
# parse irregular text
#######################################################################################
def parse(provence: str, city: list, districts: list, datetime: str):
    details = []
    citys_dict = []

    i = -1
    j = 0
    while j < len(districts) - 1:
        j += 1
        if districts[j] == '\r\n' and districts[j + 1] != '\r\n':
            if len(citys_dict) == 0 and i > 0:
                citys_dist_map = {"provence": provence,
                                  "city": city[i],
                                  "district": city[i],
                                  "datetime": datetime}
                citys_dict.append(citys_dist_map)
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
            i += 1
            continue
        else:
            if districts[j].startswith("\r\n\u3000"):
                temp = districts[j].replace('\r\n\u3000', '')
                district_list = temp.split("\u3000")

                for district in district_list:
                    if district == '':
                        continue
                    citys_dist_map = {"provence": provence,
                                      "city": city[i],
                                      "district": district,
                                      "datetime": datetime}
                    citys_dict.append(citys_dist_map)
    return details


#######################################################################################
# parse irregular text in other way
#######################################################################################


def parse2(provence: str, city: list, districts: list, datetime: str):
    details = []
    citys_dict = []

    i = -1
    j = 0
    while j < len(districts) - 1:
        j += 1

        if re.match(r'^(\u3000\u3000\d)', districts[j]) is not None or districts[j] == '\n':
            i += 1
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
            if i < len(city):
                while city[i] == '中山市' or city[i] == '东莞市':
                    citys_dist_map = {"provence": provence,
                                      "city": city[i],
                                      "district": city[i],
                                      "datetime": datetime}
                    citys_dict.append(citys_dist_map)
                    if len(citys_dict) != 0:
                        details.append(citys_dict)
                    citys_dict = []
                    i += 1
            continue
        else:
            if re.match(r'^(\u3000)\D{2,9}[区|市|县]', districts[j]) is not None:
                district_list = districts[j].split("\u3000")

                for district in district_list:
                    if district == '':
                        continue
                    citys_dist_map = {"provence": provence,
                                      "city": city[i],
                                      "district": district,
                                      "datetime": datetime}
                    citys_dict.append(citys_dist_map)
    return details


def parse2008(provence: str, city: list, districts: list, datetime: str):
    details = []
    citys_dict = []

    i = -1
    j = 0
    while j < len(districts) - 1:
        j += 1

        if districts[j] == '\r\n' and districts[j + 1] != '\r\n':
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
            i += 1
            continue
        elif i < len(city) and (city[i] == '中山市' or city[i] == '东莞市'):
            # while i+1 < len(city) and (city[i+1] == '中山市' or city[i+1] == '东莞市'):
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
            citys_dist_map = {"provence": provence,
                              "city": city[i],
                              "district": city[i],
                              "datetime": datetime}
            citys_dict.append(citys_dist_map)
            i += 1
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
        else:
            if districts[j].startswith("\r\n\u3000"):
                temp = districts[j].replace('\r\n\u3000', '')
                district_list = temp.split("\u3000")

                for district in district_list:
                    if district == '':
                        continue
                    citys_dist_map = {"provence": provence,
                                      "city": city[i],
                                      "district": district,
                                      "datetime": datetime}
                    citys_dict.append(citys_dist_map)
    return details


def parse2005(provence: str, city: list, districts: list, datetime: str):
    details = []
    citys_dict = []

    i = -1
    j = 0
    while j < len(districts) - 1:
        j += 1
        if (districts[j] == '\r\n' and districts[j + 1] != '\r\n') or \
                (districts[j] == '\n' and districts[j - 1] != '\n'):
            if len(citys_dict) == 0 and i > 0:
                citys_dist_map = {"provence": provence,
                                  "city": city[i],
                                  "district": city[i],
                                  "datetime": datetime}
                citys_dict.append(citys_dist_map)
            if len(citys_dict) != 0:
                details.append(citys_dict)
            citys_dict = []
            i += 1
            continue
        else:
            if districts[j].startswith("\r\n\u3000"):
                temp = districts[j].replace('\r\n\u3000', '')
                district_list = temp.split("\u3000")

                for district in district_list:
                    if district == '':
                        continue
                    citys_dist_map = {"provence": provence,
                                      "city": city[i],
                                      "district": district,
                                      "datetime": datetime}
                    citys_dict.append(citys_dist_map)
    return details


##################################################################################
# get text from html document
##################################################################################

def parse_city(href_, provence='广东省', datetime='2016'):
    url = get_info_url(href_)
    document = get_document(url, datetime)
    city = document.xpath('//*[@id="show"]/div[3]/strong/text()')
    districts = document.xpath('//*[@id="show"]/div[3]/text()')
    if '2008' == datetime:
        details = parse2008(provence, city, districts, datetime)
    elif '2005' == datetime:
        details = parse2005(provence, city, districts, datetime)
    else:
        details = parse(provence, city, districts, datetime)
        if len(details) == 0:
            details = parse2(provence, city, districts, datetime)
    # import ipdb;
    # ipdb.set_trace()
    return details


##################################################################################
# store into mysql
##################################################################################

def store_into_mysql(details):
    conn = get_instance()
    cursor = conn.cursor()
    for detail in details:
        for record in detail:
            cursor.execute('''insert into district(provence,\
                        city,district,datetime) values("%s","%s","%s","%s")\
                        ''' % (record["provence"], record["city"], record["district"], record["datetime"]))
    conn.commit()


#################################################################################
# store into file
#################################################################################


def store_into_file(content: str, datetime: str):
    file = open("sourcefile/district/district" + datetime + ".html", "w")
    file.write(content)
    file.close()


def request_and_store(href_='show/gd/16161.html'
                      , provence='广东省', datetime='2016'):
    details = parse_city(href_, provence, datetime)
    print(len(details))
    store_into_mysql(details)


##################################################################################
# get latest 20 years list
##################################################################################
def get_years_list():
    url = 'http://www.xzqh.org/html/list/21.html'
    document = get_document(url)
    i = 1
    while i <= 20:
        href_ = document.xpath('/html/body/div/div[4]\
                                /div[1]/ul/div/ul/li[' + str(i) + ']/a/@href')[0]
        title = document.xpath('/html/body/div/div[4]\
                                /div[1]/ul/div/ul/li[' + str(i) + ']/a/text()')[0]
        datetime = re.sub(r'\D', "", title)
        try:
            request_and_store(href_, "广东省", datetime)
        except:
            print("error: request fail: " + title)
        i += 1
