"""
-------------------------------------------------
   File Name：     douban_spider2
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
import base64
from douban_spider4 import Douban_Y

class DouBan_Spider():

    def __init__(self):
        self.proxy = '180.104.63.75:9000'

    def judge_ban(self,id,num =5):
        username = "17610086125"
        password = "cuiying1205"
        # headers = {
        #     "Accept-Encoding": "Gzip",
        #     "Proxy-Authorization": "Basic %s" % base64.b64encode(b'%s:%s'%(username,password)),
        # }
        proxies = {'http': 'http://%s' % self.proxy, }
        move_url = "https://movie.douban.com/subject/%s" % id

        try:
            response = requests.get(url=move_url,timeout=20)
        except:

                return self.judge_ban(id)
                print('请求多次仍然超时，请检查')

        html = response.text
        if html.find(r'检测到有异常请求从你的') != -1:
            print("被ban了，需要等待10s继续请求")
            time.sleep(10)
            return self.judge_ban(id)
        else:
            soup = BeautifulSoup(html, 'lxml')
            starring_name = []
            starring_id = []
            for i in soup.find_all(attrs={'rel': 'v:starring'}):
                starring_name.append(i.get_text())

                starring_id.append(i.get('href'))
            id_str = ''.join(starring_id)
            starring_id_list = re.findall(r'celebrity/(.*?)/', id_str)


            d_type=[]
            for d in  soup.find_all('span',attrs={'property':'v:initialReleaseDate'}):
                d_type.append(d.get_text())
            if d_type:
                move_date = '/'.join(d_type)
            else:
                move_date = ''



            m_type = []
            for x in soup.find_all('span',attrs={'property':'v:genre'}):

                m_type.append(x.get_text())
            if m_type :
                move_type = '/'.join(m_type)
            else:
                move_type = ''
            try:
                move_name = soup.find('span', attrs={'property': 'v:itemreviewed'}).get_text()
            except:
                move_name ='这个电影不存在了'


            try:
                move_introduction = soup.find('span', attrs={'property': 'v:summary'}).get_text()
            except:
                move_introduction =''





            try:
                move_director_name = []
                move_director_id = []
                for md in soup.find_all(attrs={'rel': 'v:directedBy'}):
                    move_director_name.append(md.get_text())
                    move_director_id.append(md.get('href'))

                id_str1 = ''.join(move_director_id)
                director_id_list = re.findall(r'/celebrity/(.*?)/', id_str1)

            except:
                director_id_list =''
            for id_2 in range(0, len(director_id_list)):
                director_id_list[id_2] = {'id': director_id_list[id_2], 'name': move_director_name[id_2]}

            try:
                move_runtime = soup.find('span', attrs={'property':"v:runtime"}).get_text()
            except:
                move_runtime = ""

            douban_y=Douban_Y()
            performer_list=douban_y.yanyuan(id)

            for id_1 in range(0,len(starring_id_list)):
                try:
                    starring_id_list[id_1]={'id':starring_id_list[id_1],'name':starring_name[id_1],'饰':performer_list[id_1]}
                except IndexError:
                    starring_id_list[id_1]={'id':starring_id_list[id_1],'name':starring_name[id_1],'饰':None}

            dic = {}
            dic['id'] = id
            dic['类型'] = move_type
            dic['名称'] = move_name
            dic['简介'] = move_introduction.strip()
            dic['导演'] = director_id_list
            # dic['主演'] = dict(zip(starring_id_list, starring_name))
            dic['主演'] = starring_id_list
            dic['时长'] = move_runtime
            dic['上映日期']=move_date
            #dic['导演id']

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
