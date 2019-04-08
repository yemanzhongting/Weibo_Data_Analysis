#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re,json
import importlib
#import string
import sys
#import os
import time
#import urllib3
#from bs4 import BeautifulSoup
import requests
from lxml import etree
import pymysql,pymongo,random
importlib.reload(sys)

cookie_list=[
    'ALF=1557200558; SCF=ArxvfZZDTxSB5JC6r-egZjQt5KAShquRTe7Jg29IQ37H4sQM1ZEKXdFE4weneteWfjltJ_xbDcrk8WSmCrL2JsU.; SUB=_2A25xreKpDeRhGeNM7loW8C7NzzuIHXVTUY7hrDV6PUJbktAKLUbikW1NSa5q31VXKWff0witHVEf13vjk9EKVMI3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW_U-piXhYkoCDoBcSWvGnm5JpX5K-hUgL.Fo-ESKnNeh5pShM2dJLoI0YLxKBLB.BL1-eLxK-LBo5L12qLxK-LB-qL1KzLxKBLBonL12-LxK-LBo5L12qLxKMLB-eLBKnLxK-L1KqLBo-t; SUHB=0h1ZFUHq-0q6lO; SSOLoginState=1554617081; _T_WM=0dd8c70ebf6c1577cbc89273eef09328',
    'SCF=ApnjEaS5A7UXAfQjcyYlarjjld5FzJoLmNjOast7L5Wyo3AfBIaoJ7fYshGkjgBNp5TcnCNend5CbYO4-Olim64.; SUB=_2A25xre5IDeRhGeBL4lcU9SnOzzqIHXVTUfIArDV6PUJbktAKLUPYkW1NRqnpi5Fq9vHhxi9WZvRk3m7nKcdhH-gS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5RYu-EBKvudoanipzWgKio5JpX5KzhUgL.Foqf1K-fSKMEShq2dJLoIceLxKnLB.BLB.zLxKnLB.BLB.zLxKqLBo-LB--LxKnLB.qL1hMLxKnL1hBLBonLxK-LB.2L1--LxKML1-2L1hBLxKML1heL1-qLxKML1hqL12qLxKMLB.-L12-LxKnL12BLBoMt; SUHB=0OMkgVYt6FpzV4; _T_WM=af05cc754b425b88d079e2d5ee1a159d; M_WEIBOCN_PARAMS=lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26luicode%3D20000174%26uicode%3D20000174; MLOGIN=1; SSOLoginState=1554619928; WEIBOCN_FROM=1110006030',
    '_T_WM=790f80c35f8372c2bfe88ece582faf87; ALF=1557225378; SCF=Av_xaKYmRjyfu-r29brXQmQ-RSfQYZp9nfXwyzhhTbvJ2aG-UQdEFbqpTyl8S0uxnQSjrL_ZgYbJkrtZm2opVk0.; SUB=_2A25xraL1DeRhGeBI7lsX-CjPyTyIHXVTUc69rDV6PUJbktANLVPtkW1NRmvUFoSJL1RPugZOW5a4JAG3OlBaOoQh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5_ymFdmJIKh.kBgEh_CClC5JpX5KzhUgL.FoqcSK.c1hq0eo52dJLoIpjLxKnL12BL1hqLxK.L1hzLBo5LxK-L12eL1hqt; SUHB=0YhRPAgiUr6Syc; SSOLoginState=1554633381; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174',
    '_T_WM=0a0a42a8d0c85048b1a008dc8b702ae5; SUB=_2A25xraMADeRhGeBI7lsX-CjPyjSIHXVTUc1IrDV6PUJbktANLVDWkW1NRmvUFnra3Vt0bHoiBNyz7GDoR3D6cS0n; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhrgFygSF17TNFS9seL4xKr5JpX5KzhUgL.FoqcSK.c1hq0eKn2dJLoIEBLxKnL1KeL1-BLxK.LBK2LB.-LxK-L1hqL1h.LxKqL1KMLBoqt; SUHB=0ebtwslrdP4rwK; SSOLoginState=1554633552; MLOGIN=1; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=uicode%3D20000174',
]

cookie = {"Cookie":"_T_WM=34d0ea094d4346b262e7eb8e06139683; SCF=AlLsH3P80Ao62KGfuThzcDF_V2b9F3rHyS8HPGam_UkgplKCFLHdlMAT2J3nl69Pdqu0ljwrRt8Pswl_FDr2Blg.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5xjrHc0koVrRuz7s7bQdQK5JpX5K-hUgL.FoqRe05pe02peK52dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMc1he7eKepeK27; SUB=_2A25xAmLNDeRhGeNM7loW8C7NzzuIHXVSDQ6FrDV6PUJbkdBeLRDkkW1NSa5q34_uT_Lfsu4_Pm5hIQXa6pJ4QltD; SUHB=0V51K96WnJjhfZ"}
                 #SCF=ApnjEaS5A7UXAfQjcyYlarjjld5FzJoLmNjOast7L5Wyo3AfBIaoJ7fYshGkjgBNp5TcnCNend5CbYO4-Olim64.; SUB=_2A25xre5IDeRhGeBL4lcU9SnOzzqIHXVTUfIArDV6PUJbktAKLUPYkW1NRqnpi5Fq9vHhxi9WZvRk3m7nKcdhH-gS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5RYu-EBKvudoanipzWgKio5JpX5KzhUgL.Foqf1K-fSKMEShq2dJLoIceLxKnLB.BLB.zLxKnLB.BLB.zLxKqLBo-LB--LxKnLB.qL1hMLxKnL1hBLBonLxK-LB.2L1--LxKML1-2L1hBLxKML1heL1-qLxKML1hqL12qLxKMLB.-L12-LxKnL12BLBoMt; SUHB=0OMkgVYt6FpzV4; _T_WM=af05cc754b425b88d079e2d5ee1a159d; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D20000174; MLOGIN=1; XSRF-TOKEN=93f81e; SSOLoginState=1554619928; WEIBOCN_FROM=1110006030
cookie={"Cookie":"SSOLoginState=1554609008; ALF=1557200672; SCF=ApnjEaS5A7UXAfQjcyYlarjjld5FzJoLmNjOast7L5WyoUPUcqHA6bXKJYL4Zfq7_scNz2VEse0P7yilTYayVIo.; SUB=_2A25xrQMgDeRhGeBL4lcU9SnOzzqIHXVTUa1orDV6PUJbktAKLVHSkW1NRqnpix9ozFkR_dr0XPxbiVw_nH-aVh0S; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5RYu-EBKvudoanipzWgKio5JpX5K-hUgL.Foqf1K-fSKMEShq2dJLoIceLxKnLB.BLB.zLxKnLB.BLB.zLxKqLBo-LB--LxKnLB.qL1hMLxKnL1hBLBonLxK-LB.2L1--LxKML1-2L1hBLxKML1heL1-qLxKML1hqL12qLxKMLB.-L12-LxKnL12BLBoMt; SUHB=0ebtzuqypPcmrV; _T_WM=af05cc754b425b88d079e2d5ee1a159d"}
def get_url(index):
    print("连接Mysql数据库读入数据...")

    db1 = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',db='URL_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor1 = db1.cursor()
    
    #str_index = 'id' + str(index)
    str_index = str(index)
    
    sql_1 = "select url from weibo_full_url where weibo_id ="+ "'" + str_index + "'" ""
 
    cursor1.execute(sql_1)
    
    result1 = cursor1.fetchall()
    
    result = result1[0]['url']
    
    db1.close()
    
    return result


def create_table(index):
    
    db3 = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',db='2017_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
    
    cursor3 = db3.cursor()
    
    sql_4 = "DROP TABLE IF EXISTS ID" + str(index)
    print(sql_4)
    
    cursor3.execute(sql_4)
    
    sql_3 = "CREATE TABLE ID" + str(index) + "(comment_num int NOT NULL AUTO_INCREMENT,user_id  VARCHAR(40),user_level VARCHAR(40),comment VARCHAR(600),PRIMARY KEY (comment_num)) default collate = utf8mb4_unicode_ci "
 
    cursor3.execute(sql_3)

    db3.close()


def write_in_database(text1,text2,text3,text4,index):
    
    db2 = pymysql.connect(host='localhost',port=3306,user='root',password='mysql',db='2017_database',charset='utf8mb4',cursorclass = pymysql.cursors.DictCursor)
 
    cursor2 = db2.cursor()
    
    sql_2 = "INSERT INTO ID" + str(index) + " (user_id,user_level,comment)" +" VALUES(%s,%s,%s)"

    cursor2.execute(sql_2,(text2,text3,text4))
    
    db2.commit()
    
    db2.close()

    
def get_url_data(base_url,pageNum,word_count,):

        
    print("爬虫准备就绪...")
    
    base_url_deal = base_url + '%d'
    
    base_url_final = str(base_url_deal)

    #print(base_url_final)

    for page in range(1,pageNum+1):

        url = base_url_final%(page)
        print(url)
        lxml = requests.get(url, cookies = cookie).content
        print('正在crawl'+str(page))
        selector = etree.HTML(lxml)

        weiboitems = selector.xpath('//div[@class="c"][@id]')

        x=random.randint(1,5)
        time.sleep(int(8+x))

        for item in weiboitems:
            weibo_id = item.xpath('./@id')[0]
            created=item.xpath('.//span[@class="ct"]/text()')[0]
            created=str(created)
            uid_name=item.xpath('./a/text()')[0]
            uid=item.xpath('./a')[0].attrib['href']
            uid=uid[3:]
            dianzan=item.xpath('./span[@class="cc"]/a/text()')[0]
            huifu=item.xpath('./span[@class="cc"]/a/text()')[1]
            text = item.xpath('./span[@class="ctt"]/text()')
            level = item.xpath('./img/@alt')
            comment=''
            if len(text)==1:
                type='评论'
                comment=text[0]
            else:
                type='回复'
                try:
                   comment=text[1]
                except IndexError:
                    comment=text

            word_count+=1
            data={

            }
            # text1 = str(word_count)
            # text2 = str(weibo_id)
            # text4 = str(ctt)
            # text3 = str(level)
            #write_in_database(text1,text2,text3,text4,index)##C_4286113747262152 > a:nth-child(1)#//*[@id="C_4286113747262152"]/a[1]
            
            #word_count += 1

    print("成功爬取！")
    print("本事件微博信息入库完毕，共%d条"%(word_count-4))


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None
#------------------------------------------------------------------------#
proxy=None
proxy_pool_url='http://127.0.0.1:5000/get'
max_count=5


def clean_text(text):
    """清除文本中的标签等信息"""
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', text)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    return dd.strip()

headers={
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
	"Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]
def get_user_agent():
    return random.choice(user_agent)


user_url='https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=230283{uid}'
def get_area(userid):
    url = user_url.format(uid=userid)
    global proxy
    count=1
    if count >= max_count:
        print('请求次数太多')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            print('利用代理访问')
            response = requests.get(url, headers=headers,allow_redirects=False,proxies=proxies)

        else:
            response = requests.get(url, headers=headers,allow_redirects=False)
        if response.status_code == 200:
            try:
                resp = json.loads(response.text)
                area = (resp['data']['cards'][0]['card_group'][0]['item_content']) if (
                    resp['data']['cards'][0]['card_group'][0]['item_content']) else None  # 转化为字典
               # print(type(area))
                return area
            except KeyError:
                pass
            except IndexError:
                pass
        if response.status_code==302:
             print('302')
             proxy=get_proxy()
             if proxy:
                 print('using proxy',proxy)
                 return get_area
             else:
                 print('代理获取不到')
                 return None
    except ConnectionError as e:
        print('Error',e.args)
        proxy=get_proxy()
        count=count+1
        return get_area

def get_mongo(base_url,pageNum,word_count,index):

    cookie = {"Cookie": random.choice(cookie_list)}

    dbname = ('范冰冰阴阳合同评论3' )#+ str(index)
    client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    db = client.comments
    #db[dbname].insert_many(data)

    print("爬虫准备就绪...")

    base_url_deal = base_url + '%d'

    base_url_final = str(base_url_deal)

    for page in range(2, pageNum + 1):
        code = 0
        url = base_url_final % (page)
        #print(url)

        cs=db[dbname].find()
        #print(cs.count())  # 获取文档个数
        for k in cs:
            if k['url']==url:
                code=1
                print('url已经存在'+url)

        if code==0:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':get_user_agent()
            }

            lxml = requests.get(url, cookies=cookie,headers=headers).content
            print('正在crawling data page' + str(page))
            print(url)
            selector = etree.HTML(lxml)

            weiboitems = selector.xpath('//div[@class="c"][@id]')

            x = random.randint(1, 20)
            time.sleep(int(8 + x))

            for item in weiboitems:
                weibo_id = item.xpath('./@id')[0]
                created = item.xpath('.//span[@class="ct"]/text()')[0]
                #created = str(created)

                month = created[2:4]
                day = created[5:7]
                comment_time = created[9:14]
                hour = comment_time[0:2]
                minute = comment_time[3:5]

                uid_name = item.xpath('./a/text()')[0]
                uid = item.xpath('./a')[0].attrib['href']
                uid = uid[3:]
                dianzan = item.xpath('./span[@class="cc"]/a/text()')[0]

                # try:
                #     dianzan = re.sub("\D", "", dianzan)
                # except:
                #     dianzan=dianzan

                huifu = item.xpath('./span[@class="cc"]/a/text()')[1]
                text = item.xpath('./span[@class="ctt"]/text()')

                try:
                   level = item.xpath('./img/@alt')[0]
                except:
                   level = item.xpath('./img/@alt')

                if len(text)==1:
                    wb_type='评论'
                    comment=text[0]
                else:
                    wb_type='回复'
                    try:
                       comment=text[1]
                    except IndexError:
                        comment=text

                #isinstance('abc', str)
                if type(comment) is dict:
                    comment=''
                #判断如果是列表则取消

                area=get_area(uid)
                word_count += 1
                data = {
                    'weibo_id':weibo_id,
                    'created':created,
                    'uid_name':uid_name,
                    'uid':uid,
                    'dianzan':dianzan,
                    'huifu':huifu,
                    #'text':text,
                    'level':level,
                    'type':wb_type,#中间运行出错，命名重复的错误
                    'comment':comment,
                    'count':word_count,
                    'area':area,
                    'url':url,
                    #详细的时间
                    "month": month,
                    "day": day,
                    #"time": comment_time,
                    "hour": hour,
                    #"minute": minute
                }
                db[dbname].insert_one(data)


    print("成功爬取！")
    print("本事件微博信息入库完毕，共%d条" % (word_count - 4))



if __name__ == '__main__':

    url_list=[
        # # 'https://weibo.cn/comment/GzW34BToG?uid=2803301701&rl=1&page=',#俄罗斯航空
        #         # # 'https://weibo.cn/comment/GzV5tvi9J?uid=2803301701&rl=1&page=',#交警查
        #         # # 'https://weibo.cn/comment/GzOC40Aie?uid=2803301701&rl=1&page=',#山竹垃圾
        #         # # 'https://weibo.cn/comment/GzNqAp1XC?uid=2803301701&rl=1&page=',#深圳人民
        #         # # 'https://weibo.cn/comment/GzLBxiTg2?uid=2803301701&rl=1&page=',
        #         # # 'https://weibo.cn/comment/GzKL5pBDq?uid=2803301701&rl=1&page=',#抢修
        #         # # 'https://weibo.cn/comment/GzJeliGw6?uid=2803301701&rl=1&page=',#港珠澳大桥
        #         # #'https://weibo.cn/comment/GzC21nTh0?uid=1642512402&rl=1&page=',#中国新闻周刊
        #         # 'https://weibo.cn/comment/GzKfr5VuY?uid=1618051664&rl=1&page=',#头条新闻
        #         # 'https://weibo.cn/comment/GzkFLCfSK?uid=1974576991&rl=1&page=',#环球时报
        #         # 'https://weibo.cn/comment/Gzm80vldd?uid=1686546714&rl=1&page=',#环球网关于台风山竹
        #         # 'https://weibo.cn/comment/GzurSiueS?uid=2803301701&rl=1&page=',#风王台风
        #         # 'https://weibo.cn/comment/GzkXswras?uid=2803301701&rl=1&page=',#台风

        'https://weibo.cn/comment/GCbgmgCUA?uid=1647688972&rl=1&page=',  # 环球人物杂志VM :【税务部门依法查处范冰冰“阴阳合同”等偷逃税问题
        'https://weibo.cn/comment/GjUYqlC0Q?rl=1&page=',  # 新京报VM :【崔永元：范冰冰痛哭向我道歉，阴阳合同还有大人物】

        'https://weibo.cn/comment/GCaS4tTjK?uid=1642591402&rl=1&page=',#新浪娱乐，
        'https://weibo.cn/comment/GCaKsdwq5?uid=1974576991&rl=1&page=',#环球时报，刑事调查
        'https://weibo.cn/comment/GCaN1w498?uid=1726918143&rl=1&page=',#中国青年报调查
        'https://weibo.cn/comment/GCWyJ4pZ5?uid=1642591402&rl=1&page=',#新浪娱乐，范冰冰案件不等于不判刑
        'https://weibo.cn/comment/GCdaE7bNZ?uid=1644114654&rl=1&page=',#新京报，体现司法宽严相济
        'https://weibo.cn/comment/GCb2CDI8o?uid=1191965271&rl=1&page=',#三联生活周刊，范冰冰涉税问题
        'https://weibo.cn/comment/GCaKGoEAt?uid=1988800805&rl=1&page='#凤凰网财经，依法惩治
    ]

    longth=len(url_list)

    for index in range(0,longth):
        
        word_count = 1
        
        #base_url = get_url(index)
        base_url=url_list[index]

        print(base_url)

        first_url = base_url + '1'

        cookie = {"Cookie":random.choice(cookie_list)}

        html = requests.get(first_url,cookies = cookie).content
        selector = etree.HTML(html)
        
        controls = selector.xpath('//input[@name="mp"]')
        
        if controls:
            pageNum = int(controls[0].attrib['value'])#word_count初试为1
        else:
            pageNum = 1
        print(index)

        try:
           get_mongo(base_url,pageNum,word_count,index)
        except Exception as e:  # 抓住所有错误,一般放在最后
            print("未知错误", e)
            print('此条没有抓取成功' + str(index))
        else:
            print("进行下一条微博爬取...")

        index=index+1

    print("全部完成！")
