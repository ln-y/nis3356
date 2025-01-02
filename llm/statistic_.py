import matplotlib.pyplot as plt
import os
import json
from scipy.stats import entropy
import numpy as np
import re

re_er = re.compile(r'emotion_new_cache(\d*)(_*).json')
print(re_er.findall('emotion_new_cache5.json'))
all_dic = {}
for fi in os.listdir():
    # if fi.startswith('emotion_new_cache'):
    #     breakpoint()
    matches = re_er.findall(fi)
    if matches:
        if matches[0][0]:
            index_num = int(matches[0][0])
        else:
            index_num = 0
        if matches[0][1] == '_':
            index_num = index_num + 0.5
        with open(fi, 'r', encoding='utf-8') as f:
            data = json.load(f)
            statistic_dic = {}
            for val in data.values():
                if val not in statistic_dic:
                    statistic_dic[val] = 1
                else:
                    statistic_dic[val] += 1
            print(statistic_dic)
            all_dic[index_num] = entropy(list(statistic_dic.values()))
print(all_dic)
key_lst = list(all_dic.keys())
key_lst.sort()
key_lst.remove(3)
key_lst.remove(8)
val_lst = [all_dic[k] for k in key_lst]
plt.plot(val_lst)
plt.title('prompt engineer for better classify')
plt.xlabel('version')
plt.ylabel('entropy')
plt.savefig('0.png',dpi=320)