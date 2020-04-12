import requests
import pymysql
import re
from bs4 import BeautifulSoup
class covid():
    def __init__(self):
        # self.url = 'http://news.163.com/special/epidemic/'
        self.url = 'https://wp.m.163.com/163/page/news/virus_report/index.html?_nw_=1&_anw_=1'
        # self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        self.header = {'user-agent': 'Mozilla/5.0'}
        # self.conn = pymysql.connect(host="localhost", port=3306, database='covid', user='root', password='qq654321')
        self.conn = pymysql.connect(host="47.107.67.23", port=3306, database='covid', user='root', password='caren6211430')
        self.all_confirm = 0
        self.all_dead = 0
        self.all_heal = 0
        self.time_info = ''
        self.info_list = []

    def GetData(self):
        # req = requests.get(self.url, headers=self.header, timeout=30)
        # req.raise_for_status()
        # req.encoding = req.apparent_encoding
        # text = req.text
        f = open("covidReport.html", "r+", encoding='utf-8')
        text = f.read()
        f.close()
        soup = BeautifulSoup(text, 'html.parser')
        # —————————国内疫情数据提取—————————
        title = soup.find('div', attrs={'class':'cover_data_china'})
        number_class_list = title.findAll('div', attrs={'class': 'number'})
        self.all_confirm = number_class_list[3].string
        self.all_dead = number_class_list[4].string
        self.all_heal = number_class_list[5].string
        time = title.find('div', attrs={'class': 'cover_time'}).text
        self.time_info = re.findall(r"截至(.+?)数据说明", time)[0]
        # ——————————各省市疫情数据提取———————————
        detail = soup.findAll('li', attrs={'class': 'hasCities active'})
        for item in detail:
            province = item.find('div', attrs={'class': 'province'})
            info = province.findAll('span')
            province_name = info[0].string
            province_nconfirm = info[1].string.strip()
            if len(province_nconfirm) == 0:
                province_nconfirm = 0
            province_confirm = info[2].string
            province_dead = info[3].string
            province_heal = info[4].string
            # print(province_name, province_confirm, province_dead, province_heal)
            self.info_list.append((province_name, province_name, province_confirm, province_nconfirm, province_dead, province_heal))
            cities = item.findAll('li')
            for city in cities:
                c_info = city.findAll('span')
                city_name = c_info[0].string
                city_nconfirm = c_info[1].string.strip()
                if len(city_nconfirm) == 0:
                    city_nconfirm = 0
                # province_nconfirm.replace(' ', '0')
                city_confirm = c_info[2].string
                city_dead = c_info[3].string
                city_heal = c_info[4].string
                # print(city_name, city_confirm, city_dead, city_heal)
                self.info_list.append((province_name, city_name, city_confirm, city_nconfirm, city_dead, city_heal))
            #     break
            # break

    '''
    def SaveData(self, sql):
        pass
    '''

if __name__ == '__main__':
    Covid = covid()
    Covid.GetData()
    # 获取数据库连接
    cs = Covid.conn.cursor()
    sql = "INSERT INTO myapp_allinfo(confirm, dead, heal, time_info) values({}, {}, {}, '{}')".format(Covid.all_confirm, Covid.all_dead, Covid.all_heal, Covid.time_info)
    print(sql)
    cs.execute(sql)
    Covid.conn.commit()
    # for info in Covid.info_list:
    #     # sql = "INSERT INTO myapp_mxinfo(province, name, confirm, suspect, dead, heal, time_info) values ({}, {}, {}, {}, {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5], Covid.time_info)
    #     sql = "INSERT INTO myapp_mxinfo(province, name, confirm, suspect, dead, heal, time_info) "
    #     sql += "values ('{}', '{}', {}, {}, {}, {}, '{}')".format(info[0], info[1], info[2], info[3], info[4], info[5], Covid.time_info)
    #     print(info[0], info[1], info[2], info[3], info[4], info[5])
    #     print(sql)
    #     print(type(info[3]))
    #     cs.execute(sql)
    #     Covid.conn.commit()
    cs.close()
    Covid.conn.close()