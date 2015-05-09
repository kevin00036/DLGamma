import os
from os.path import join as pjoin
import sys
import string
import re

def qmap(mp, x):
    if x not in mp: return 0
    return mp[x]

def amap(mp, x):
    if x not in mp: mp[x] = 0
    mp[x] += 1

DATA_PATH = '../data'
TRAIN_PATH = pjoin(DATA_PATH, 'Holmes_Training_Data')
TEST_PATH = pjoin(DATA_PATH, 'testing_data.txt')

filename_list = os.listdir(TRAIN_PATH)
test_data_raw = list(open(TEST_PATH))
test_data_raw = [x.strip('\n') for x in test_data_raw]

mp_word = {}
mp_bigram = {}

for cnt, filename in enumerate(filename_list):
    # if cnt >= 10: break
    print('Reading', cnt, filename)
    rs = open(pjoin(TRAIN_PATH, filename), encoding='latin-1').read()
    rs = rs.replace('-\n', '')
    rs = re.split('[^a-zA-Z0-9-\']', rs)
    rs = list(filter(lambda x: x, rs))
    rs = [x.lower() for x in rs]

    for i in rs:
        amap(mp_word, i)
    # for i in zip(rs[:-1], rs[1:]):
        # if i not in mp_bigram: mp_bigram[i] = 0
        # mp_bigram[i] += 1
    for i in range(0, len(rs)-6):
        we = rs[i]
        for j in range(1, 6):
            he = rs[i+j]
            amap(mp_bigram, (we, he))
            amap(mp_bigram, (he, we))

test_data = []
ques = []
ques_bigram = []
for i in range(len(test_data_raw)//5):
    rr = test_data_raw[i*5:(i+1)*5]
    rr = [x[x.find(' ')+1:] for x in rr]
    rr = [re.split('[^a-zA-Z0-9-\'\[\]]', x) for x in rr]
    rr = [list(filter(lambda y: y, x)) for x in rr]

    qs = []
    ctx = []
    for j in rr:
        ls = [x.lower() for x in j]
        for k, s in enumerate(ls):
            if s[0] == '[':
                qs.append(s[1:-1])
                ctx = j[:k] + j[k+1:]
    ques.append(qs)
    ques_bigram.append(ctx)

ans_list = []
english = 'abcde'

for qs, ctx in zip(ques, ques_bigram):
    print(qs, ctx)
    w1 = qmap(mp_word, ctx[0]) + 1
    w2 = qmap(mp_word, ctx[1]) + 1
    ans_id = -1
    best_score = -1
    for c, i in enumerate(qs):
        score = 1
        for j in ctx:
            score += qmap(mp_bigram, (j, i))
        if score > best_score:
            ans_id = c
            best_score = score
        print(i, score)
    print(ans_id, qs[ans_id])
    ans_list.append(english[ans_id])

f = open('output2.txt', 'w')
f.write('id,answer\n')
for i, j in enumerate(ans_list):
    f.write('{},{}\n'.format(i+1, j))
