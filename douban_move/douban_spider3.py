"""
-------------------------------------------------
   File Name：     douban_spider3
   Description :
   Author :       zws
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""
__author__ = 'zws'

from Do_Excel import DoExcel
import requests
import re
from bs4 import BeautifulSoup
import time
from My_Proxy import  My_Proxy
import random


class DouBan_Spider():

    def __init__(self):
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'}
        self.ip_list = ['180.104.63.75：9000','115.223.217.216:9000']
        self.my_proxy = My_Proxy()

    def judge_ban(self,id,num =5):
        move_url = "https://movie.douban.com/subject/%s" % id
        try:
            response = requests.get(url=move_url,headers=self.user_agent,timeout=20)

        except:
            if num !=1:
                num-=1
                return self.judge_ban()
            else:
                print('请求多次仍然超时，请检查')

        html = response.text
        if html.find(r'检测到有异常请求从你的') != -1:
            print("准备切换代理")
            IP = ''.join(random.choice(self.ip_list).strip())
            proxy = {'http': IP}
            print('正在切换代理')
            print('当前代理：', proxy)
            return requests.get(url=move_url,headers=self.user_agent,proxies=proxy)






            # time.sleep(600)
            # return self.judge_ban(id)
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
            for x in soup.find_all('span',attrs={'property':'v:genre'}):
                m_type.append(x.get_text())
            if m_type :
                move_type = '/'.join(m_type)
            else:
                move_type = ''
            try:
                move_name = soup.find('span', attrs={'property': 'v:itemreviewed'}).get_text(encoding='GB18030')
            except:
                print('这本书不存在了')

            try:
                move_introduction = soup.find('span', attrs={'property': 'v:summary'}).get_text(encoding='GB18030')
            except:
                move_introduction =''
            try:
                move_director = soup.find(rel="v:directedBy").get_text(encoding='GB18030')
            except:
                move_director =''

            try:
                move_runtime = soup.find('span', attrs={'property':"v:runtime"}).get_text(encoding='GB18030')
            except:
                move_runtime = ""


            for id_1 in range(0,len(starring_id_list)):
                starring_id_list[id_1]={'id':starring_id_list[id_1],'name':starring_name[id_1]}


            dic = {}
            dic['id'] = id
            dic['类型'] = move_type
            dic['名称'] = move_name
            dic['简介'] = move_introduction.strip()
            dic['导演'] = move_director
            # dic['主演'] = dict(zip(starring_id_list, starring_name))
            dic['主演'] = starring_id_list
            dic['时长'] = move_runtime

            print(dic)

            with open('move.txt', 'a',encoding='utf-8') as f:
                f.write(str(dic) + '\n')
                f.close()



if __name__ == '__main__':
    m = DouBan_Spider()
    do_excel = DoExcel('move_id.xlsx')
    id_list = do_excel.get_id()
    for m_id in id_list:
        m.judge_ban(m_id)