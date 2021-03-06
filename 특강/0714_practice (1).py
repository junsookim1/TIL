# -*- coding: utf-8 -*-
"""0714_practice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NqOByV2D2KleWH_vrVE5ATT5D8rZNJUl

## Bow

### from sklearn.feature_extraction.text import CountVectorizer
"""

from sklearn.feature_extraction.text import CountVectorizer

docs = ['오늘 동물원에서 원숭이를 봤어',
        '오늘 동물원에서 코끼리를 봤어 봤어',
        '동물원에서 원숭이에게 바나나를 줬어 바나나를']

cout_vect = CountVectorizer()
Bow = cout_vect.fit_transform(docs)
Bow.toarray()[0] # 첫번째 문장에 대한 bow

Bow.toarray()

import pandas as pd

from IPython.core import display as ICD

vocab = cout_vect.get_feature_names() # sorting 할 필요는 없다! 순서가 맞기 때문에 
for i in range(len(docs)):
    print('문서 {} : {}'.format(i, docs[i]))
    ICD.display(pd.DataFrame([Bow.toarray()[i]], columns=vocab))

"""### gensim"""

import gensim
from gensim import corpora

docs = ['오늘 동물원에서 원숭이를 봤어',
        '오늘 동물원에서 코끼리를 봤어 봤어',
        '동물원에서 원숭이에게 바나나를 줬어 바나나를']

doc_ls = [doc.split() for doc in docs]

id2word = corpora.Dictionary(doc_ls)

Bow = [id2word.doc2bow(doc) for doc in doc_ls]

Bow[0]

from gensim.matutils import sparse2full

from IPython.core import display as ICD

vocab = [id2word[i] for i in id2word.keys()]

for i in range(len(docs)):
    print('문서 {} : {}'.format(i, docs[i]))
    ICD.display(pd.DataFrame([sparse2full(Bow[i], len(vocab))], columns=vocab))

"""###tdm
- 2차원 행렬로 만들기
"""

docs = ['오늘 동물원에서 원숭이를 봤어',
        '오늘 동물원에서 코끼리를 봤어 봤어',
        '동물원에서 원숭이에게 바나나를 줬어 바나나를']

doc_ls = [doc.split() for doc in docs]
doc_ls

from collections import defaultdict

word2id = defaultdict(lambda : len(word2id))
[word2id[token] for doc in doc_ls for token in doc ]     
word2id

import numpy as np

TDM = np.zeros((len(word2id), len(doc_ls)), dtype=int) # 2차원 행렬 정렬
for i, doc in enumerate(doc_ls):
    for token in doc:
        TDM[word2id[token], i] += 1
TDM

"""###sklearn 이용"""

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
DTM = count_vect.fit_transform(docs)
DTM.toarray()

import pandas as pd

doc_names = ['문서' + str(i) for i in range(len(doc_ls))]
vocab = count_vect.get_feature_names()
df_TDM = pd.DataFrame(DTM.T.toarray(), columns=doc_names) #T-transposit TDM으로 나온다.
df_TDM['단어'] = vocab # '단어'열을 만들어주고
df_TDM.set_index('단어') #set_index로 배열

"""# TF-IDF (Term Frequency-Inverse Document Frequency)"""

docs = ['오늘 동물원에서 원숭이를 봤어',
        '오늘 동물원에서 코끼리를 봤어 봤어',
        '동물원에서 원숭이에게 바나나를 줬어 바나나를']

"""### 1) 띄어쓰기 단위로 토큰화"""

doc_ls = [doc.split() for doc in docs]
doc_ls

"""### 2) 각 고유 토큰에 인덱스(index)를 지정"""

#dic만들어 주기
from collections import defaultdict

word2id = defaultdict(lambda : len(word2id))

for doc in doc_ls: # [word2id[token] for in doc_ls for token in doc] 
    for token in doc:
        word2id[token]
word2id

"""### 3)DTM 생성"""

import numpy as np
TDM = np.zeros((len(word2id), len(doc_ls)), dtype=int) # 2차원 행렬 8행 3열
print(len(word2id))
print(len(doc_ls))
for i, doc in enumerate(doc_ls):
    for token in doc:
        TDM[word2id[token], i] += 1
TDM

DTM = TDM.T
DTM

"""### 4) TF계산"""

DTM.sum

def computeTF(DTM):
    doc_len = len(DTM)
    word_len = len(DTM[0])  

    tf = np.zeros((doc_len, word_len))

    for doc_i in range(doc_len):
        for word_i in range(word_len):
            tf[doc_i, word_i] = DTM[doc_i, word_i]/DTM[doc_i].sum() #list의 값들을 합의 함수 sum

    return tf


tf = computeTF(DTM)
tf

"""IDF"""

import math

def computeITF(DTM):
    doc_len = len(DTM)
    word_len = len(DTM[0])  

    idf = np.zeros(word_len)
    for i in range(word_len):
        idf[i] = -math.log10(np.count_nonzero(DTM[:, i]) /doc_len)
    
    return idf



computeITF(DTM)

"""###TF-IDF계산"""

def computeTFITF(DTM):
    tf = computeTF(DTM)
    idf = computeITF(DTM)

    tfidf = np.zeros(tf.shape)
    for doc_i in range(tf.shape[0]):
       for word_i in range(tf.shape[1]):
         tfidf[doc_i, word_i] = tf[doc_i, word_i] * idf[word_i]
    
    return tfidf

computeTFITF(DTM)

import pandas as pd
##
sorted_vocab = sorted((value, key) for key, value in word2id.items())
vocab = [v[1] for v in sorted_vocab]
tfidf= computeTFIDF(DTM)
pd.DataFrame(tfidf, columns=vocab)



