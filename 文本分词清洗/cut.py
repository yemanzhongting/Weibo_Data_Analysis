
_author_ = 'zy'
import jieba,pymongo,time

jieba.load_userdict("SogouLabDic.txt")
jieba.load_userdict("dict_baidu_utf8.txt")
jieba.load_userdict("dict_pangu.txt")
jieba.load_userdict("dict_sougou_utf8.txt")
jieba.load_userdict("dict_tencent_utf8.txt")
jieba.load_userdict("my_dict.txt")
#FILE_OBJECT= open('order.log','r', encoding='UTF-8')
stopwords = {}.fromkeys([ line.rstrip() for line in open('Stopword.txt',encoding='UTF-8') ])

listkeyword=['全文','链接','视频','网页']
def ch_segj(text):
    seg=jieba.cut(text)
    return seg
def get_data(dbname):
    client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    db = client.comments
    cursor=db[dbname].find()#segmentation   "segmentation"
    result=[]
    for i in cursor:
        comment=i['comment']
        if type(comment)==str:
            seg = jieba.cut(comment)
            thiscomment=""
            for j in seg:
                if j not in stopwords:
                    if j!=' ':
                        if j not in listkeyword:
                            thiscomment=thiscomment+j+' '#,

            result.append(thiscomment.rstrip(','))  # 列表list.append
######################可注释
            data={
                "segmentation":thiscomment.rstrip(',')
            }
            mongoid = i['_id']
            myquery = {"_id": mongoid}
            newvalues = {"$set": data}
            db[dbname].update_one(myquery, newvalues)
##########
    fo = open("jieba_all", "w+",encoding='UTF-8')#, encoding='UTF-8'
    # fo = open("/Users/kimmeen/Downloads/P_Weibo/%s"%user_id, "w")

    for k in result:#列表结构
        #print(type(j))
        #print(type(result))
        fo.write(k)
        fo.write('\r\n')
    fo.close()
if __name__ == '__main__':

    starttime = time.time()
    print("进程开始...")
    get_data('范冰冰阴阳合同评论3')
    print("Done!")
    endtime = time.time()
    print(endtime - starttime)
