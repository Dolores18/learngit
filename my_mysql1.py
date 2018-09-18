from pyquery import PyQuery as pq # 导入解析库
import pymysql # 用于连接并操作MySQL数据库

import requests
import re
def get_html(url):
    r = requests.get(url)
    return r
def pare_html(content):
    
    my_way = re.compile('class="title".*?>(.*?)</span>.*?"v:average">(.*?)</span>.*?"10.0">.*?<span>(.*?)</span>.*?"inq">(.*?)</span>',re.S)
    titles = re.findall(my_way, content.text)
    
    for titles in titles:
        mydict = {}
        mydict['title']=titles[0]
        mydict['rating'] = titles[1]
        mydict['pn'] = titles[2]
        mydict['rm'] = titles[3]
        
        yield mydict


    
def main():
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i * 25)
        content = get_html(url)
        connection = pymysql.connect(host='localhost', # 连接数据库
                                     user='root',
                                     password='mtjbydd11', # 你安装mysql时设置的密码
                                     db='ganji',
                                     charset='utf8',
                                     
                                     cursorclass=pymysql.cursors.DictCursor)
        sql = "insert into douban3 (title, rating, pn, rm)values(%s,%s,%s,%s)"
        try:
            with connection.cursor() as cursor:
                for item in pare_html(content):
                    cursor.execute(sql, (
                        item['title'], item['rating'],item['pn'],item['rm']))
            connection.commit() # 提交刚刚执行的SQL处理，使其生效
        finally:
            connection.close()   
if __name__ == '__main__':
    main()