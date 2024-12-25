import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import json

with open("stop_words_cn.txt","r", encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())
stopwords.add("\n")
stopwords.add("plaintext")
stopwords.add("comment")
stopwords.add("Comment")

re_er= re.compile(r'2024-[\d\-\s,:]+ - root - INFO - Output (\d+) generated')

import jieba
from collections import Counter
import re

platformid_dic = {'shuiyuan': 0, 'bilibili': 31, 'douyin': 115}
emotion_abstact_dic = {}
tmp_lst = []
now_ind = -1
with open("abstract_em_0.json","r", encoding='utf-8') as f:
    data = json.load(f)

def get_freq(text):
    text = re.sub(r'[^\w\n]', '', text)

    chinese_words = jieba.lcut(text)

    # 英文分词，这里使用正则表达式匹配英文单词
    english_words = re.findall(r'[A-Za-z]+', text)

    # 合并中英文分词结果
    all_words = chinese_words + english_words
    # 打印词频统计结果
    # for word, freq in word_freq.most_common(10):
    #     print(f"{word}: {freq}")

    filtered_words = [word for word in all_words if word not in stopwords]
    filtered_word_freq = Counter(filtered_words)

    return filtered_word_freq
plt.rcParams['font.sans-serif'] = ['FangSong'] 
def draw_bar_chart(save_path, data, title, x_label, y_label, x_label_name):
    '''
    示例数据：x对应的的y值总数无需归一化
    x_label = ['人群A', '人群B', '人群C']

    y_label = ['食品', '娱乐', '交通', '通讯']

    data = {
        '人群A': [30, 20, 25, 25],
        '人群B': [20, 25, 30, 25],
        '人群C': [25, 20, 25, 30]
    }
    '''

    # 归一化data
    for ki, vi in data.items():
        totali = sum(vi)
        for i in range(len(vi)):
            data[ki][i] = 100 * data[ki][i] / totali
    

    # 创建堆叠条形图
    plt.figure(figsize=(12, 7.2))
    fig, ax = plt.subplots()
    bottom = [0] * len(x_label)

    for ind, yi in enumerate(y_label):
        percentages = [data[xi][ind] for xi in x_label]
        ax.bar(x_label, percentages, bottom=bottom, label=yi, width=0.35)
        bottom = [bottom[i] + percentages[i] for i in range(len(x_label))]

    # 设置图表标题和标签
    ax.set_title(title)
    ax.set_ylabel('百分比%')
    ax.set_xlabel(x_label_name)
    ax.set_ylim(0, 100)  # 设置y轴范围

    # 添加图例
    ax.legend(fontsize = 8)

    # 显示图表
    plt.savefig(save_path, dpi=320)
    plt.cla()

output_lst = [i["output"] for i in data]

all_chars = '\n'.join(output_lst)
freq_dic = get_freq(all_chars)
wordcloud = WordCloud(width=1600, height=800, background_color='white', margin= 5, max_words=70, 
                        font_path=r"C:\Users\000\AppData\Local\Microsoft\Windows\Fonts\SmileySans-Oblique.otf").generate_from_frequencies(freq_dic)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.savefig("emotion.png",dpi=480)

shuiyuan_chars = '\n'.join(output_lst[:31])
bilibili_chars = '\n'.join(output_lst[31:115])
douyin_chars = '\n'.join(output_lst[115:])

dic_char = {
    "shuiyuan": shuiyuan_chars,
    "bilibili": bilibili_chars,
    "douyin": douyin_chars,
    "all": all_chars
}
all_key_set = set()
res_dic = {}
for key,val in dic_char.items():
    freq_dic = get_freq(val).most_common()
    others_num = sum([i[1] for i in freq_dic[9:]])
    new_freq_dic = freq_dic[:8] + [("Others", others_num)]
    res_dici = {i[0]:i[1] for i in new_freq_dic}
    res_dic[key] = res_dici
    all_key_set = all_key_set | set(res_dici.keys())
data_dic = {}
all_key_set.remove('Others')
all_key_lst = list(all_key_set)
all_key_lst.sort()
for key,val in res_dic.items():
    data_dic[key] = [val.get(i, 0) for i in all_key_lst]
draw_bar_chart("platform.png", data_dic, "各平台情感词频", list(dic_char.keys()), all_key_lst, "平台")





