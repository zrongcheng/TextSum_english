import word_emb
import numpy as np

file_num=9#文件数量
data_dir=[r'F:\Bytecup2018\processed\train{}.txt'.format(i) for i in range(file_num)]
title_dir=[r'F:\Bytecup2018\processed\title\deal_title\train_title{}.txt'.format(i)
            for i in range(file_num)]

#1.给出vocab
data,_=word_emb.load_data(data_dir,title_dir,file_num)
total_data=[]
for i in range(file_num):
    total_data+=data[i]
vocab_path=r'F:\Bytecup2018\vocab\vocab.txt'
vocab_size=100000#词汇表单词数量
word_emb.create_vocabulary(total_data,vocab_path,vocab_size)

#2.调用vocab
word2idx,idx2word=word_emb.initialize_vocabulary(vocab_path)

##3.降维，通过glove为每个单词学习一个低维向量
filename = r'F:\glove.6B.50d.txt'
embed_dict,embed_size = word_emb.loadGloVe(filename)
trainable_tokens=idx2word[:4]
for token in trainable_tokens:
    print("    %s" % token)
    if token not in embed_dict:
        embed_dict[token] = [0.0] * embed_size
embed_mat = np.array(
      [embed_dict.get(token,embed_dict['_UNK']) for token in idx2word], dtype=np.float32)
