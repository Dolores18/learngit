#
from selenium import webdriver
from bs4 import BeautifulSoup
import re
driver=webdriver.Chrome()
import os
import requests


url = 'https://music.163.com/#/artist?id=16152'
driver.get(url)
driver.switch_to.frame(driver.find_element_by_name("contentFrame"))
html = driver.page_source
bsObj = BeautifulSoup(html, 'html.parser')
dataList = bsObj.findAll(name = 'a', attrs = {'href':re.compile(r'/song.id=\d{1,10}')})
for data in dataList[2:]:
    
    ids = data.get('href')
    num = re.search(r'\d{1,10}', ids)
    number = num.group()
    print(number)

    name = (data.text)
    print(name)
music_url = 'http://music.163.com/song/media/outer/url?id=' + str(number)+'.mp3'
try:
    music = requests.get(music_url)
    print('正在下载……')
except:
    print('下载失败')


path = r'F:\music12'
if not os.path.isdir(path):
    os.makedirs(path)
with open ('F:\music12\%s.mp3'% name, 'wb') as f:
    f.write(music.content)
    print('下载成功')
      

driver.close()   