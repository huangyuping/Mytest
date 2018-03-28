"""
-------------------------------------------------
   File Name：     douban_spider4
   Description :
   Author :       小鱼
   date：          2018/3/27
-------------------------------------------------
   Change Activity:
                   2018/3/27:
-------------------------------------------------
"""
__author__ = '小鱼'
from Do_Excel import DoExcel
import requests
import re
from bs4 import BeautifulSoup
import time


class Douban_Y():
    def yanyuan(self,id):
        sta_name_list = []
        move_url_star = 'https://movie.douban.com/subject/%s/celebrities'%id
        try:
            response1 = requests.get(url=move_url_star, timeout=20)
        except:

            return self.yanyuan(id)
            print('请求多次仍然超时，请检查')

        html1 = response1.text
        if html1.find(r'检测到有异常请求从你的') != -1:
            print("被ban了，需要等待10s继续请求")
            time.sleep(10)
            return self.yanyuan(id)
        else:
            sta_name = re.findall(r''' <span class="role" title="(.*?)">''',html1)
            # for sta in soup1.find_all(title=re.compile('饰')):
            #     sta_name.append(sta.get_text())
        for i in sta_name:
            sta_name_list.append(i.replace("饰 ",''))
        return sta_name_list


#                sta_str3 = ''.join(sta_name).replace("饰 ",'')
#
#                 print("..........")
#                 print(sta_str3)




if __name__ == '__main__':
    m = Douban_Y()
    do_excel = DoExcel('move_id.xlsx')
    id_list = do_excel.get_id()
    for m_id in id_list:
        m.yanyuan(m_id)
