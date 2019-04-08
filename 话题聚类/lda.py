#-*- coding:utf-8 -*-

import logging
import logging.config
import configparser
import numpy as np
import random
import codecs
import os

import matplotlib.pyplot as plt




from collections import OrderedDict
path = os.getcwd()
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
# loggerInfo = logging.getLogger("TimeInfoLogger")
# Consolelogger = logging.getLogger("ConsoleLogger")

conf = configparser.ConfigParser()
conf.read('setting.conf')

trainfile = os.path.join(path,os.path.normpath(conf.get("filepath", "trainfile")))
wordidmapfile = os.path.join(path,os.path.normpath(conf.get("filepath","wordidmapfile")))
thetafile = os.path.join(path,os.path.normpath(conf.get("filepath","thetafile")))
phifile = os.path.join(path,os.path.normpath(conf.get("filepath","phifile")))
paramfile = os.path.join(path,os.path.normpath(conf.get("filepath","paramfile")))
topNfile = os.path.join(path,os.path.normpath(conf.get("filepath","topNfile")))
tassginfile = os.path.join(path,os.path.normpath(conf.get("filepath","tassginfile")))

K = int(conf.get("model_args","K"))
alpha = float(conf.get("model_args","alpha"))
beta = float(conf.get("model_args","beta"))
iter_times = int(conf.get("model_args","iter_times"))
top_words_num = int(conf.get("model_args","top_words_num"))

class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0

class DataPreProcessing(object):

    def __init__(self):
        self.docs_count = 0
        self.words_count = 0
        self.docs = []
        self.word2id = OrderedDict()

    def cachewordidmap(self):
        with codecs.open(wordidmapfile, 'w','utf-8') as f:
            for word,id in self.word2id.items():
                f.write(word +"\t"+str(id)+"\n")

class LDAModel(object):
    
    def __init__(self,dpre):

        self.dpre = dpre 
        self.K = K
        self.beta = beta
        self.alpha = alpha
        self.iter_times = iter_times
        self.top_words_num = top_words_num 
        self.wordidmapfile = wordidmapfile
        self.trainfile = trainfile
        self.thetafile = thetafile
        self.phifile = phifile
        self.topNfile = topNfile
        self.tassginfile = tassginfile
        self.paramfile = paramfile
        self.p = np.zeros(self.K)        
        self.nw = np.zeros((self.dpre.words_count,self.K),dtype="int")       
        self.nwsum = np.zeros(self.K,dtype="int")    
        self.nd = np.zeros((self.dpre.docs_count,self.K),dtype="int")       
        self.ndsum = np.zeros(dpre.docs_count,dtype="int")    
        self.Z = np.array([ [0 for y in range(dpre.docs[x].length)] for x in range(dpre.docs_count)])

        for x in range(len(self.Z)):
            self.ndsum[x] = self.dpre.docs[x].length
            for y in range(self.dpre.docs[x].length):
                topic = random.randint(0,self.K-1)
                self.Z[x][y] = topic
                self.nw[self.dpre.docs[x].words[y]][topic] += 1
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1

        self.theta = np.array([ [0.0 for y in range(self.K)] for x in range(self.dpre.docs_count) ])
        self.phi = np.array([ [ 0.0 for y in range(self.dpre.words_count) ] for x in range(self.K)]) 
    
    def sampling(self,i,j):

        topic = self.Z[i][j]
        word = self.dpre.docs[i].words[j]
        self.nw[word][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1

        Vbeta = self.dpre.words_count * self.beta
        Kalpha = self.K * self.alpha
        self.p = (self.nw[word] + self.beta)/(self.nwsum + Vbeta) * \
                 (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)
        
        p = np.squeeze(np.asarray(self.p/np.sum(self.p)))
        topic = np.argmax(np.random.multinomial(1, p))

        self.nw[word][topic] +=1
        self.nwsum[topic] +=1
        self.nd[i][topic] +=1
        self.ndsum[i] +=1

        return topic
    
    def est(self):
        for x in range(self.iter_times):
            for i in range(self.dpre.docs_count):
                for j in range(self.dpre.docs[i].length):
                    topic = self.sampling(i,j)
                    self.Z[i][j] = topic
        logger.info(u"迭代完成。")
        logger.debug(u"计算文章-主题分布")
        self._theta()
        logger.debug(u"计算词-主题分布")
        self._phi()
        logger.debug(u"保存模型")
        self.save()
    
    def _theta(self):
        for i in range(self.dpre.docs_count):
            self.theta[i] = (self.nd[i]+self.alpha)/(self.ndsum[i]+self.K * self.alpha)
    
    def _phi(self):
        for i in range(self.K):
            self.phi[i] = (self.nw.T[i] + self.beta)/(self.nwsum[i]+self.dpre.words_count * self.beta)
    
    def save(self):
        logger.info(u"文章-主题分布已保存到%s" % self.thetafile)
        
        with codecs.open(self.thetafile,'w') as f:
            for x in range(self.dpre.docs_count):
                for y in range(self.K):
                    f.write(str(self.theta[x][y]) + '\t')
                f.write('\n')
        
        logger.info(u"词-主题分布已保存到%s" % self.phifile)
        
        with codecs.open(self.phifile,'w') as f:
            for x in range(self.K):
                for y in range(self.dpre.words_count):
                    f.write(str(self.phi[x][y]) + '\t')
                f.write('\n')
        
        logger.info(u"参数设置已保存到%s" % self.paramfile)
        
        with codecs.open(self.paramfile,'w','utf-8') as f:
            f.write('K=' + str(self.K) + '\n')
            f.write('alpha=' + str(self.alpha) + '\n')
            f.write('beta=' + str(self.beta) + '\n')
            f.write(u'迭代次数  iter_times=' + str(self.iter_times) + '\n')
            f.write(u'每个类的高频词显示个数  top_words_num=' + str(self.top_words_num) + '\n')
        
        logger.info(u"主题topN词已保存到%s" % self.topNfile)

        with codecs.open(self.topNfile,'w','utf-8') as f:
            self.top_words_num = min(self.top_words_num,self.dpre.words_count)#这个还做了一个放报错，来进行处理最小top词语
            for x in range(self.K):
                f.write(u'第' + str(x) + u'类：' + '\n')
                twords = []
                #x从10个挑选结果
                twords = [(n,self.phi[x][n]) for n in range(self.dpre.words_count)]#在所有词语,phi代表对主题的贡献率,生成twords的list
                twords.sort(key = lambda i:i[1], reverse= True)

                for y in range(self.top_words_num):
                    word = OrderedDict({value:key for key, value in self.dpre.word2id.items()})[twords[y][0]]
                    f.write('\t'*2+ word +'\t' + str(twords[y][1])+ '\n')

        
        logger.info(u"文章-词-主题分派结果已保存到%s" % self.tassginfile)
        
        with codecs.open(self.tassginfile,'w') as f:
            for x in range(self.dpre.docs_count):
                for y in range(self.dpre.docs[x].length):
                    f.write(str(self.dpre.docs[x].words[y])+':'+str(self.Z[x][y])+ '\t')
                f.write('\n')
        
        logger.info(u"模型训练完成。")


def preprocessing():
    logger.info(u'载入数据......')
    with codecs.open(trainfile, 'r','utf-8') as f:
        docs = f.readlines()
    logger.debug(u"载入完成,准备生成字典对象和统计文本数据...")
    dpre = DataPreProcessing()
    items_idx = 0
    for line in docs:
        if line != "":
            tmp = line.strip().split()
            doc = Document()
            for item in tmp:
                if item in dpre.word2id :
                    doc.words.append(dpre.word2id[item])
                else:
                    dpre.word2id[item] = items_idx
                    doc.words.append(items_idx)
                    items_idx += 1
            doc.length = len(tmp)
            dpre.docs.append(doc)
        else:
            pass
    dpre.docs_count = len(dpre.docs)
    dpre.words_count = len(dpre.word2id)
    logger.info(u"共有%s个文档" % dpre.docs_count)
    dpre.cachewordidmap()
    logger.info(u"词与序号对应关系已保存到%s" % wordidmapfile)
    return dpre#dpre好像是文档个数
#model-phi为主题贡献率,每一行代表一个主题，每一个数字代表对主题的贡献率，
#theta为，每一行文档，文档中每一个数字代表某主题对文档的贡献，所以空的话都为0.1
# #这个矩阵特别大,也就说这句话更偏向哪个聚类，加起来总共为100
#tassign每一行代表文档，表示文档中，每个词语与其匹配的主题
#phi有十行，K行，很多次列
#E:\Githubresponsity\weibo1123\step5_LDA\data\tmp
def plotpic():
    n=top_words_num
    file_path_name="聚类结果.txt"
    f = open('聚类结果.txt', "r",encoding='utf-8')
    i=1  #b%a
    list=[]
    for line in f:
        #print(line)
        ys=i%(n+1)
        #cluster=int(ys/21)
        #print(ys)
        i=i+1
        if ys!=1:
            result=str(line).split('\t')
            #print(result)
            keyword=result[0]
            prob=result[1]
            prob=float(prob)
            print(keyword+' '+prob)
            #print(keyword + '\t' + prob)
            data={
                keyword:prob
            }
            list.append(data)
    #
    # for j in K:
    print (list)

def draw():
    f, ax = plt.subplots(5, 1, figsize=(8, 6), sharex=True)
    for i, k in enumerate([0, 5, 9, 14, 19]):
        ax[i].stem(topic_word[k, :], linefmt='b-',
                   markerfmt='bo', basefmt='w-')
        ax[i].set_xlim(-50, 4350)
        ax[i].set_ylim(0, 0.08)
        ax[i].set_ylabel("Prob")
        ax[i].set_title("topic {}".format(k))

    ax[4].set_xlabel("word")

    plt.tight_layout()
    plt.show()

def run():
    dpre = preprocessing()
    lda = LDAModel(dpre)
    lda.est()
    
if __name__ == '__main__':
    run()
    #plotpic()
    #https://github.com/KimMeen/Weibo-Analyst
    # α ：表示
    # document - topic
    # 密度， α
    # 越高，文档包含的主题更多，反之包含的主题更少
    #
    # β ：表示
    # topic - word
    # 密度， β
    # 越高，主题包含的单词更多，反之包含的单词更少