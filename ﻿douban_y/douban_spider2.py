"""
-------------------------------------------------
   File Name：     douban_spider2
   Description :
   Author :       小鱼
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""
import urllib

__author__ = '小鱼'
from Do_Excel import DoExcel
import requests
import re
import time
from urllib.request import urlretrieve, urlcleanup
import os

class DouBan_Spider():
    def auto_down(self,url, filename):
        try:
            urlretrieve(url, filename)
        except :
            print("重新下载")
            urlcleanup()
            return self.auto_down(url,filename)
    def judge_ban(self, id):
        move_url = "https://movie.douban.com/celebrity/%s" % id
        try:
            response = requests.get(url=move_url, timeout=30)
        except:
                time.sleep(10)
                print('请求多次仍然超时，请检查')
                return self.judge_ban(id)
        html = response.text
        if html.find(r'检测到有异常请求从你的') != -1:
            print("被ban了，需要等待10s继续请求")
            time.sleep(10)
            return self.judge_ban(id)
        else:
            picture = r'''title="点击看大图"
                src="(.*?)">'''
            imgre = re.compile(picture)
            imgrelist = imgre.findall(html)
        if imgrelist!=[]:
            self.auto_down(imgrelist[0],os.getcwd()+'/picture/%s.jpg'%id)
            print("当前演员id为:" + str(id))
            print('.......................')
        else:
            print("该演员没有头像")
            print('.......................')
if __name__ == '__main__':
    m = DouBan_Spider()
    do_excel = DoExcel('move_id.xlsx')
    id_list = do_excel.get_id()
    count = 0
    for m_id in id_list:
        count += 1
        print('当前下载了' + str(count) + '张')
        m.judge_ban(m_id)
