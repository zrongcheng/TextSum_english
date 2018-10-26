from collections import Counter


_PAD = r"_PAD"
_GO = r"_GO"
_EOS = r"_EOS"
_UNK = r"_UNK"#词汇表外的词用UNK_ID表示
_START_VOCAB = [_PAD, _GO, _EOS, _UNK]

PAD_ID = 0
GO_ID = 1
EOS_ID = 2
UNK_ID = 3

def load_data(data_dir,title_dir,file_num=9):

    train_data=[None]*file_num #文章
    train_title=[None]*file_num #标题

    #读取处理好的文章，和标题 train_data=[train_data1,...],train_data1是列表
    for i in range(file_num):
        with open(data_dir[i],'r+',encoding='utf-8') as f:
            train_data[i] = [line for line in f]
        with open(title_dir[i],'r+',encoding='utf-8') as ff:
            train_title[i]=[line for line in ff]
    return train_data,train_title

def create_vocabulary(data,vocabulary_path,max_vocabulary_size):
    #创建并保存词汇表
    vocab = Counter(w for txt in data for w in txt.split())
    vocab_list = _START_VOCAB+sorted(vocab, key=vocab.get,reverse=True)#list类型

    if len(vocab_list) > max_vocabulary_size:
        vocab_list = vocab_list[:max_vocabulary_size]
    print("Save vocab...")
    with open(vocabulary_path, 'w+',encoding='utf-8') as vocab_file:
        for w in vocab_list:
            vocab_file.write(w)
            vocab_file.write('\n')
    # with open(r'F:\Bytecup2018\vocab\vocabcount.txt', 'w+', encoding='utf-8') as vocab_file:
    #     for w in vocab_list:
    #         vocab_file.write(w)
    #         vocab_file.write(' '+str(vocab[w]))#词频
    #         vocab_file.write('\n')
    print("Save completed...")

def initialize_vocabulary(vocabulary_path):
    # 确定单词在词汇表中的位置
    #读取词汇表为一个字典，并将词汇表reverse（这个操作可以通过将键存储为一个list来完成）
    # vocab：{"dog": 0, "cat": 1}=word2idx ; rev_vocab：["dog", "cat"]=idx2word
    idx2word = []
    with open(vocabulary_path, 'r+',encoding='utf-8') as f:
        idx2word.extend(f.readlines())
    idx2word = [line.strip() for line in idx2word]
    word2idx = dict([(x, y) for (y, x) in enumerate(idx2word)])

    return word2idx, idx2word

#token_ids应用于one hot标识，仅供参考
def sentence_to_token_ids(sentence, vocabulary):
    #把句子转换成token_id,(list)
    '''a sentence "I have a dog" may become tokenized into
    ["I", "have", "a", "dog"] and with vocabulary {"I": 1, "have": 2,
    "a": 4, "dog": 7"} this function will return [1, 2, 4, 7].'''

    words=sentence.split()
    return [vocabulary.get(w, UNK_ID) for w in words]
#同上
def data_to_token_ids(data_dir, title_dir,tokens_path,title_tokens_path,
                      vocabulary_path,file_num=9):
    #把所有句子转换成token_id，并存储
    print('load data...')
    data , title = load_data(data_dir,title_dir,file_num)
    print('initial vocab...')
    word2idx,_=initialize_vocabulary(vocabulary_path)
    print('Starting...')
    for i in range(file_num):
        #将内容转成数字标识
        with open(tokens_path[i],'w+',encoding='utf-8') as tokens:
            for line in data[i]:
                token_ids=sentence_to_token_ids(line,word2idx)
                tokens.write(" ".join([str(token) for token in token_ids]) + "\n")
        print('tokens{} completed'.format(i))
        #将标题转成数字标识
        with open(title_tokens_path[i],'w+',encoding='utf-8') as tokens:
            for line in title[i]:
                title_ids=sentence_to_token_ids(line,word2idx)
                tokens.write(" ".join([str(token) for token in title_ids]) + "\n")
        print('  title_tokens{} completed'.format(i))

def loadGloVe(embed_file):
    # 为词汇表中的所有单词学习一个嵌入，嵌入：即用向量表示单词
    embd_dict=dict()
    with open(embed_file,'r',encoding='utf-8') as file:
        i=0
        for line in file.readlines():
            row = line.strip().split(' ')#string格式
            word = row[0]
            vec = list(map(float, row[1:]))
            embd_dict[word] = vec
            embed_size=len(vec)#向量维度
            i+=1
            if i % 100000 == 0:
                print('{} lines completed'.format(i))
    print('Loaded GloVe!')
    return embd_dict,embed_size