# TextSum_english
Get the title of an English article

1.src_data_deal

    对原数据进行清洗。
    去除特殊字符；
    对日期、链接、数字等进行泛化处理；
    最后对文章和标题分别存储。

2.word_emb
    
    把清洗后的所有数据分词；
    将所有单词进行counter统计，取前100000个单词，再加上4个标记，存储到vocab.txt；
    最后为vocab中的所有单词学习一个嵌入，用的是预训练好的GloVe文件进行学习

3.train_process
    
    对word_emb进行调用
