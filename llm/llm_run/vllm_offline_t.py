from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams
from transformers import AutoTokenizer

import os
import tqdm
import pickle, json

version = 0
from config import model_name
model_choice = ["姜萍", "王闰秋", "阿里巴巴", "新闻媒体", "教育制度", "其他评论者", "无法判断"]
prompt = f'''\
请仔细阅读以下评论区的对话，并仅对最后一个评论所评论的主体进行分类。判断其评论目标是以下六个主体中的哪一个：

* 姜萍
* 王闰秋
* 阿里巴巴
* 新闻媒体
* 教育制度
* 其他评论者

如果最后一个评论的内容与上述主体都不相关，或者含糊不清，无法确定其评价的主体，请归类为“无法判断”。

以下是评论分析的具体指导：

1. **姜萍**：评论中包含对姜萍或其行为的评价，如“主=6”、“jp”等。
2. **王闰秋**：评论中包含对姜萍老师的评价，如“老师”、“教师”等。
3. **阿里巴巴**：评论中包含了对竞赛组委会的评价，如“阿里”、“竞赛”、“作弊”等。
4. **新闻媒体**：评论中包含了媒体报道的评价，如“谣言”、“回旋镖”、“流量”等。
5. **教育制度**：评论中包含了对教育制度的评价，如“高考”、“中专”等。
6. **其他评论者**：评论中包含了对其他评论者的评价，如“小丑”等。

示例评论分析：

1. 
[Conversation]
comment0:"主：是不是很6？"
[Last Comment]
comment0:"主：是不是很6？"
分类结果：姜萍

2.
[Conversation]
comment30:"一个破自媒体搞得跟正规军一样，发新闻都不调查清楚或者故意不清楚"
[Last Comment]
comment30:"一个破自媒体搞得跟正规军一样，发新闻都不调查清楚或者故意不清楚"
分类结果：新闻媒体

3.
[Conversation]
comment127:"永无止尽的八月在95日迎来结局
事实证明，主流媒体确实是六流媒体，阿里的公关倒是优秀公关"
[Last Comment]
comment127:"永无止尽的八月在95日迎来结局
事实证明，主流媒体确实是六流媒体，阿里的公关倒是优秀公关"
分类结果：阿里巴巴

4.
[Conversation]
comment39:"只能说高考埋没了不少有天赋的人才，那些对数学有天赋有兴趣的孩子本该可以十七十八岁真正的钻研数学，却因为应付高考，时间用在刷一遍又一遍毫无意义的“数学”题。"
[Last Comment]
comment39:"只能说高考埋没了不少有天赋的人才，那些对数学有天赋有兴趣的孩子本该可以十七十八岁真正的钻研数学，却因为应付高考，时间用在刷一遍又一遍毫无意义的“数学”题。"
分类结果：教育制度

5.
[Conversation]
comment1275:"可能不是天才，但是差也差不到哪里去吧，起码比我强，早忘了高数什么线性代数概率论偏微分方程"
comment2041:"回复 @凼篁 :小丑关你什么事"
[Last Comment]
comment2041:"回复 @凼篁 :小丑关你什么事"
分类结果：其他评论者

6.
[Conversation]
comment2384:"签到题（"
[Last Comment]
comment2384:"签到题（"
分类结果：无法判断

7.
[Conversation]
comment214:"这种老师你不开除？造成这么大的社会影响，说是诈骗都不为过，最后只是取消本年度的评先资格？你无敌了"
[Last Comment]
comment214:"这种老师你不开除？造成这么大的社会影响，说是诈骗都不为过，最后只是取消本年度的评先资格？你无敌了"
分类结果：王闰秋

请根据这些指导对以下对话中的Last Comment进行分类：
[[Comment]]
分类结果：'''

guided_decoding_params = GuidedDecodingParams(choice=model_choice)
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, guided_decoding=guided_decoding_params, seed=42) # 

llm = LLM(model = model_name, gpu_memory_utilization= 0.95, enforce_eager=True, max_num_seqs= 128, enable_prefix_caching=True)

data_flst = os.listdir('data')
tag_lst = []
prompt_lst = []
comment_lst = []
for fi in data_flst:
    if fi.endswith('.pkl'):
        with open(f"data/{fi}","rb") as f:
            queries_dic = pickle.load(f)
        f_name = fi.split('.')[0]
        for k,v in queries_dic.items():
            tag_lst.append(f"{f_name}_{k}")
            v = v.replace('\n\nNow, classify the sentiment of last comment.','')
            prompt_lst.append(prompt.replace("[[Comment]]", v ))
            comment_lst.append(v)
# progress_bar = tqdm(total=len(queries),desc="processing")
print(len(tag_lst))
with open(f"t_v{version}.log","w") as f:
    f.write(str(len(tag_lst))+"\n")
    for i in [0,512,2048]:
        f.write(prompt_lst[i]+"\n"+"="*50+"\n")

print(llm.generate(prompts=prompt_lst[0], sampling_params=sampling_params))
outputs = llm.generate(prompts=prompt_lst, sampling_params=sampling_params)

output_lst = []
for ind, outputi in enumerate(outputs):
    output_lst.append({"tag":tag_lst[ind], "prompt": comment_lst[ind], "output": outputi.outputs[0].text})
with open(f"output/t_output_{version}.json","w") as f:
    json.dump(output_lst,f, indent=4, ensure_ascii=False)
