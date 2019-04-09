#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re,json
import importlib
import sys
import time
import requests
from lxml import etree
import pymysql,pymongo,random
importlib.reload(sys)
import configparser
import os
import random_agent
#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/spider.ini'
    config.read(path)
    return config.get(section, key)
#其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
#c_list = getConfig("CookiePool")#, "cookie_list"

with open('cookie','r+',encoding='utf-8') as f:
    cookie_list=f.readlines()
with open('url','r+',encoding='utf-8') as f:
    url_list=f.readlines()
cookie = {"Cookie":""}

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

user_url='https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=230283{uid}'
max_count=3
def get_area(userid):
    #获得用户所在地
    url = user_url.format(uid=userid)
    count=1
    try:
        if count >= max_count:
            print('请求次数太多')
            return None
        response = requests.get(url, headers=headers,allow_redirects=False)
        if response.status_code == 200:
            try:
                resp = json.loads(response.text)
                area = (resp['data']['cards'][0]['card_group'][0]['item_content']) if (
                    resp['data']['cards'][0]['card_group'][0]['item_content']) else None  # 转化为字典
                return area
            except KeyError:
                pass
            except IndexError:
                pass

    except ConnectionError as e:
        print('Error',e.args)
        count=count+1
        return get_area

def get_mongo(base_url,pageNum,word_count,index):

    cookie = {"Cookie": random.choice(cookie_list)}

    dbname = ('范冰冰阴阳合同评论0409' )#+ str(index)
    client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    db = client.comments

    print("爬虫准备就绪...")

    base_url_deal = base_url + '%d'

    base_url_final = str(base_url_deal)

    for page in range(2, pageNum + 1):
        code = 0
        url = base_url_final % (page)

        cs=db[dbname].find()
        #print(cs.count())  # 获取文档个数
        for k in cs:
            if k['url']==url:
                code=1
                print('url已经存在'+url)

        if code==0:
            #抓取成功
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':random_agent.get_user_agent()
            }

            lxml = requests.get(url, cookies=cookie,headers=headers).content
            print('正在crawling data page' + str(page))
            print(url)
            selector = etree.HTML(lxml)
            weiboitems = selector.xpath('//div[@class="c"][@id]')

            x = random.randint(1, 20)
            time.sleep(int(8 + x))
             #爬虫休息
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

                    'level':level,
                    'type':wb_type,
                    'comment':comment,
                    'count':word_count,
                    'area':area,
                    'url':url,

                    "month": month,
                    "day": day,
                    "hour": hour,
                }
                db[dbname].insert_one(data)

    print("成功爬取！")
    print("本事件微博信息入库完毕，共%d条" % (word_count - 4))

if __name__ == '__main__':



    longth=len(url_list)

    for index in range(0,longth):
        
        word_count = 1

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
