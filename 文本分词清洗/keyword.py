# -*- coding: UTF-8 -*-
_author_ = 'zy'
_date_ = '2018/11/23 0023 16:13'

from jieba import analyse

tfidf = analyse.extract_tags

for line in open("jieba_all",encoding='UTF-8'):

    text = line
    keywords = tfidf(text, allowPOS=('ns', 'nr', 'nt', 'nz', 'nl', 'n', 'vn', 'vd', 'vg', 'v', 'vf', 'a', 'an', 'i'))

    result = []

    for keyword in keywords:
        result.append(keyword)

    # print(result)
    fo = open("data_keywords_non.dat", "a+",encoding='UTF-8')

    for j in result:
        print(j)
        fo.write(j)
        fo.write(' ')

    fo.write('\n')
    fo.close()

print("Keywords Extraction Done!")

