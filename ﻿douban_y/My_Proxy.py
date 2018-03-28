"""
-------------------------------------------------
   File Name：     My_Proxy
   Description :
   Author :       zws
   date：          2018/3/20
-------------------------------------------------
   Change Activity:
                   2018/3/20:
-------------------------------------------------
"""
__author__ = 'zws'

import requests
import re
import random
import time

class My_Proxy():

    def __init__(self):
        self.ip_list=['180.104.63.75：9000','115.223.217.216:9000'


        ]

        self.user_agent_list = [
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
        ]

    def get(self,url,proxy=None,timeout=20,num=5):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA}

        if proxy == None:
            html = requests.get(url,headers=headers,timeout=timeout).text
            if html.find(r'检测到有异常请求从你的') != -1:
                IP = ''.join(random.choice(self.ip_list).strip())
                proxy = {'http': IP}
                print('正在切换代理')
                print('当前代理：', proxy)
                return self.get(url, proxy=proxy, timeout=timeout)



            # try:
            #     return requests.get(url,headers=headers,timeout=timeout)
            # except:
            #     if num > 0:
            #         time.sleep(10)
            #         return self.get(url,num = num-1)
            #     else:
            #         time.sleep(10)
            #         IP = ''.join(random.choice(self.ip_list).strip())
            #         proxy={'http':IP}
            #         print('正在切换代理')
            #         print('当前代理：', proxy)
            #         return self.get(url,proxy=proxy,timeout=timeout)


        else:
            try:
                IP =''.join(random.choice(self.ip_list).strip())
                proxy = {'http':IP}
                return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
            except:
                if num >0:
                    time.sleep(10)
                    IP = ''.join(random.choice(self.ip_list).strip())
                    proxy = {'http':IP}
                    print('正在切换代理')
                    print('当前代理：',proxy)
                    return self.get(url,proxy=proxy,num=num-1)
