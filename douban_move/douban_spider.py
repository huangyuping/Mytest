"""
-------------------------------------------------
   File Name：     douban_spider
   Description :
   Author :       zws
   date：          2018/3/19
-------------------------------------------------
   Change Activity:
                   2018/3/19:
-------------------------------------------------
"""
__author__ = 'zws'
from Do_Excel import DoExcel
import requests
import re
from bs4 import BeautifulSoup
import time


do_excel =DoExcel('move_id.xlsx')
id_list = do_excel.get_id()



for i_ in id_list:
    move_url ="https://movie.douban.com/subject/%s"%i_
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
    response = requests.get(url=move_url,timeout =10)
    html = response.text

    if html.find(r'检测到有异常请求从你的') != -1:
        time.sleep(600)
        continue
    else:
        soup = BeautifulSoup(html, 'lxml')
        starring_name = []
        starring_id = []
        id_ = ''
        for i in soup.find_all(attrs={'rel': 'v:starring'}):
            starring_name.append(i.get_text())
            starring_id.append(i.get('href'))
        id_str = ''.join(starring_id)
        starring_id_list = re.findall(r'celebrity/(.*?)/', id_str)

        m_type = []
        for x in soup.find_all(attrs={'property':'v:genre'}):
            m_type.append(x.get_text())
        print(m_type)



        move_name = soup.find('span', attrs={'property': 'v:itemreviewed'}).get_text()
        move_introduction = soup.find('span', attrs={'property': 'v:summary'}).get_text()
        move_type = soup.find_all(attrs={'property':'v:genre'})
        move_director = soup.find(rel="v:directedBy").get_text()
        move_runtime = soup.find('span', attrs={'property': "v:runtime"}).get_text()

        dic = {}
        dic['id'] = i_
        dic['类型']= move_type
        dic['名称'] = move_name
        dic['简介'] = move_introduction.strip()
        dic['导演'] = move_director
        dic['主演'] = dict(zip(starring_id_list,starring_name))
        dic['时长'] = move_runtime

        print(dic)

        with open('move.txt','a') as f:
            f.write(str(dic)+'\n')
            f.close()






