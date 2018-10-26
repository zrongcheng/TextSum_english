# -*- coding:utf-8 -*-
import json
import re

file_num=9
data_dir=[r'F:\Bytecup2018\bytecup.corpus.train.{}.txt'.format(i) for i in range(file_num)]#文件绝对地址
data=[None]*file_num
for i in range(file_num):
    with open(data_dir[i],'r+') as f:
        data[i] = [json.loads(line) for line in f]

_WORD_SPLIT = re.compile(r"([.,!“\[\]\-/–—/”?\"\n:;…)(]|[^a-zA-Z\'])")
_DATA=re.compile(r'((January|February|March|April|May|June|'
                 r'July|August|September|October|November|December) \d{1,2}, \d{4})|'
                 r'((January|February|March|April|May|June|'
                 r'July|August|September|October|November|December) \d{4})|'
                 r'((January|February|March|April|May|June|'
                 r'July|August|September|October|November|December) \d{1,2})|'
                 r'(\b(January|February|March|April|May|June|'
                 r'July|August|September|October|November|December)\b)')
_DIGIT=re.compile(r"\b\d+\b")
_URL=re.compile(r'((https|http)\:\/\/[a-zA-Z0-9\.\/\-_]+)|(www.[a-zA-Z0-9\.\/\-_]+)')

#save content to flie
for i in range(file_num):
    with open(r'F:\Bytecup2018\processed\train{}.txt'.format(i),
              'w+',encoding='utf-8') as ff:
        for j in range(len(data[i])):
            words=data[i][j]['content']
            words = words.lower()  # 大写转小写
            words=re.sub(_URL,'TAGURL',words)#替换链接
            words=re.sub(_DATA,'TAGDATA',words)#替换日期
            words=re.sub(_DIGIT,'TAGDIGIT',words)#替换单独数字
            words = re.sub(r'\d+', ' ', words)#替换在字母中的数字
            words = re.sub('’', '\'', words)
            words=re.sub(_WORD_SPLIT,' ', words)#替换特殊字符
            words = re.sub(r'(\s\')|(\'\s)', ' ', words)#替换单引号单词

            ff.write(words)
            ff.write('\n')
    print('train{} completed'.format(i))

#save title to file
for i in range(file_num):
    with open(r'F:\Bytecup2018\processed\title\deal_title\train_title{}.txt'.format(i),
              'w+',encoding='utf-8') as ff:
        for j in range(len(data[i])):
            head=data[i][j]['title']
            head = head.lower()  # 大写转小写
            head = re.sub(_URL, 'TAGURL', head)  # 替换链接
            head = re.sub(_DATA, 'TAGDATA', head)  # 替换日期
            head = re.sub(_DIGIT, 'TAGDIGIT', head)  # 替换单独数字
            head = re.sub(r'\d+', ' ', head)  # 替换在字母中的数字
            head = re.sub('’', '\'', head)
            head = re.sub(_WORD_SPLIT, ' ', head)  # 替换特殊字符
            head = re.sub(r'(\s\')|(\'\s)', ' ', head)  # 替换单引号单词

            ff.write(head)
            ff.write('\n')
    print('train_title{} completed'.format(i))
