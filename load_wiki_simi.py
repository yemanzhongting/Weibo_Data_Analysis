# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2019/4/7 22:26'
import gensim

import sys

model = gensim.models.Word2Vec.load(r'D:\BaiduNetdiskDownload\wiki\word2vec_wiki.model')

word1='typhoon'
word2='apple'
sim_100=u'港珠澳大桥'
# 计算两个词语相似度
print('计算'+word1+'与'+word2+'的相似度')
y = model.similarity(word1, word2)
print (y)