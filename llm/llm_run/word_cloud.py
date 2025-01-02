import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import json

with open("stop_words_cn.txt","r") as f:
    stopwords = set(f.read().splitlines())
stopwords.add("\n")
stopwords.add("plaintext")

re_er= re.compile(r'2024-.* - root - INFO - .*')

import jieba
from collections import Counter
import re

with open("app.log","r") as f:
    chars = f.read()
# 中英文混合文本
text = re_er.sub("", chars)
text = re.sub(r'[^\w\n]', '', text)

# 中文分词
chinese_words = jieba.lcut(text)

# 英文分词，这里使用正则表达式匹配英文单词
english_words = re.findall(r'[A-Za-z]+', text)

# 合并中英文分词结果
all_words = chinese_words + english_words

# 统计词频
word_freq = Counter(all_words)

# 打印词频统计结果
# for word, freq in word_freq.most_common(10):
#     print(f"{word}: {freq}")

filtered_words = [word for word in all_words if word not in stopwords]
filtered_word_freq = Counter(filtered_words)

# 打印排除停用词后的词频统计结果
with open("emotion_dic.json","w") as f:
    json.dump(filtered_word_freq.most_common(),f,ensure_ascii=False,indent=4)
# for word, freq in filtered_word_freq.most_common(10):
#     print(f"{word}: {freq}")

wordcloud = WordCloud(width=800, height=400, background_color='white', font_path="BB4171.TTF").generate_from_frequencies(filtered_word_freq)

# 显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.savefig("emotion.png",dpi=720)