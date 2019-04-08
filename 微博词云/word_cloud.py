#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:06:18 2017
@author: Ming JIN
"""
import jieba.analyse
from PIL import Image,ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
from wordcloud import WordCloud,ImageColorGenerator
#import matplotlib.mlab as mlab    

font = FontProperties(fname='Songti.ttc')  
bar_width = 0.5
lyric= ''
#data_keywords.dat
f=open('data_keywords_non.dat','r',encoding='UTF-8')#C:\Users\83804\Desktop\Weibo-Analyst-master\step3_word_cloud
#请输入关键字生成的的目录，上一步keyword已经生成
for i in f:
    lyric+=f.read()

result=jieba.analyse.textrank(lyric,topK=50,withWeight=True)

keywords = dict()
for i in result:
    keywords[i[0]]=i[1]
print(keywords)#输出一个字典的形式

image= Image.open('./background.png')
graph = np.array(image)
wc = WordCloud(font_path='Songti.ttc',background_color='White',max_words=3000,max_font_size=50,min_font_size=0.1)#mask=graph,
wc.generate_from_frequencies(keywords)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis("off")
plt.show()
wc.to_file('词云图.png')

X=[]  
Y=[] 

for key in keywords:
    
    X.append(key)
    Y.append(keywords[key])

num = len(X)
   
fig = plt.figure(figsize=(28,10))  
plt.bar(range(num),Y,tick_label = X,width = bar_width)
#plt.xlabel("X-axis",fontproperties=font)  
#plt.ylabel("Y-axis",fontproperties=font)
plt.xticks(rotation = 50,fontproperties=font,fontsize=20)
plt.yticks(fontsize=20)
plt.title("归一化词频直方图",fontproperties=font,fontsize=11)
plt.savefig("归一化词频直方图.jpg",dpi = 360)
plt.show()