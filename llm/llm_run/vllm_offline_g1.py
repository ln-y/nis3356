from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams
from transformers import AutoTokenizer

import os
import tqdm
import pickle, json

version = 4
from config import model_name
model_choice = ["认可", "质疑", "批判", "反思", "讽刺", "无法判断"]
prompt = f'''\
请仔细阅读以下评论区的对话，并仅对最后一个评论进行观点分类。判断其支持以下五个观点中的哪一个：

认可：对姜萍及其行为的认可和支持
质疑：质疑参赛结果的真实性与姜萍的数学能力
批判：批判新闻传播带来的误导效应
反思：反思现有教育系统存在的缺陷
讽刺：讽刺姜萍的数学能力与姜萍支持者对姜萍的认可

如果最后一个评论的内容与上述观点都不相关，或者含糊不清，无法确定其支持的观点，请归类为“无法判断”。

以下是评论分析的具体指导：

1. **认可**：评论中包含对姜萍或其行为的正面评价，如“支持”、“致敬”等。
2. **质疑**：评论中对参赛结果的真实性或姜萍的数学能力表示怀疑，如“没得洗”、“结果可疑”、“作弊”等。
3. **批判**：评论中批评了新闻传播的不实信息或误导效应，如“误导”、“假新闻”、“信息不对称”等。
4. **反思**：评论中讨论了教育系统的问题或需要改进的地方，如“教育不公”、“系统缺陷”、“需要改革”等。
5. **讽刺**：评论中讽刺了姜萍及其支持者或相关事件，如“洗地”、“幽默”、“主=6”等。

示例评论分析：

1. 
[Conversation]
comment48:"致敬每一个有所热爱的人"
[Last Comment]
comment48:"致敬每一个有所热爱的人"

分类结果：认可

2.
[Conversation]
comment59:"虽然但是，我还是觉得很扯，从同济高数到谢惠民再到evans，这就很从炼气到金丹再到大乘一样，根本不符合数学学习的正常规律啊 :exploding_head:"
[Last Comment]
comment59:"虽然但是，我还是觉得很扯，从同济高数到谢惠民再到evans，这就很从炼气到金丹再到大乘一样，根本不符合数学学习的正常规律啊 :exploding_head:"

分类结果：质疑

3.
[Conversation]
comment1909:"少阴阳了，了解下报刊的有机运动和动态报道"
comment1911:"一手抓黑流量，一手抓澄清流量，两手抓，两手都要硬"
[Last Comment]
comment1911:"一手抓黑流量，一手抓澄清流量，两手抓，两手都要硬"

分类结果：批判

4.
[Conversation]
comment39:"只能说高考埋没了不少有天赋的人才，那些对数学有天赋有兴趣的孩子本该可以十七十八岁真正的钻研数学，却因为应付高考，时间用在刷一遍又一遍毫无意义的“数学”题。"
[Last Comment]
comment39:"只能说高考埋没了不少有天赋的人才，那些对数学有天赋有兴趣的孩子本该可以十七十八岁真正的钻研数学，却因为应付高考，时间用在刷一遍又一遍毫无意义的“数学”题。"
分类结果：反思

5.
[Conversation]
comment0:"该说不说，知乎上质疑派还是算占了上风的"
[Last Comment]
comment0:"该说不说，知乎上质疑派还是算占了上风的"

分类结果：质疑

6.
[Conversation]
comment2384:"签到题（"
[Last Comment]
comment2384:"签到题（"

分类结果：无法判断

7.
[Conversation]
comment69:"真心祝福当初拼命给姜萍洗地的姐妹们各个貌若杨笠，智如姜萍，寿比佳佳[给心心][给心心][给心心]"
[Last Comment]
comment69:"真心祝福当初拼命给姜萍洗地的姐妹们各个貌若杨笠，智如姜萍，寿比佳佳[给心心][给心心][给心心]"

分类结果：讽刺

8.
[Conversation]
comment0:"主：是不是很6？"
[Last Comment]
comment0:"主：是不是很6？"

分类结果：讽刺

9.
[Conversation]
comment40:"新闻三要素：时效性真实性新鲜性，你是一个都没有啊"
[Last Comment]
comment40:"新闻三要素：时效性真实性新鲜性，你是一个都没有啊"

分类结果：批判

请根据这些指导对以下对话中的Last Comment进行分类：
'''

prompt2 = '''
分类结果应为以下之一：
- 认可
- 质疑
- 批判
- 反思
- 讽刺
- 无法判断
'''

guided_decoding_params = GuidedDecodingParams(choice=model_choice)
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, guided_decoding=guided_decoding_params, seed=42) # 

llm = LLM(model = model_name, gpu_memory_utilization= 0.95, enforce_eager=True, max_num_seqs= 128, enable_prefix_caching=True)
tokenizer = AutoTokenizer.from_pretrained(model_name)

data_flst = os.listdir('data')
tag_lst = []
prompt_tk_lst = []
prompt_lst = []
bg_tk = tokenizer(prompt)["input_ids"]
ed_tk = tokenizer(prompt2)["input_ids"]
for fi in data_flst:
    if fi.endswith('.pkl'):
        with open(f"data/{fi}","rb") as f:
            queries_dic = pickle.load(f)
        f_name = fi.split('.')[0]
        for k,v in queries_dic.items():
            tag_lst.append(f"{f_name}_{k}")
            v = v.replace('\nNow, classify the sentiment of last comment.','')
            mid_tk = tokenizer(v)["input_ids"]
            prompt_tk_lst.append(bg_tk + mid_tk + ed_tk)
            prompt_lst.append(v)
prompt_tk_lst = prompt_tk_lst[:2049]
# progress_bar = tqdm(total=len(queries),desc="processing")
print(len(tag_lst))
with open(f"g_v{version}.log","w") as f:
    f.write(str(len(tag_lst))+"\n")
    for i in [0,512,2048]:
        f.write(tokenizer.decode(prompt_tk_lst[i])+"\n"+"="*50+"\n")

print(llm.generate(prompt_token_ids=prompt_tk_lst[0], sampling_params=sampling_params))
outputs = llm.generate(prompt_token_ids=prompt_tk_lst, sampling_params=sampling_params)

output_lst = []
for ind, outputi in enumerate(outputs):
    output_lst.append({"tag":tag_lst[ind], "prompt": prompt_lst[ind], "output": outputi.outputs[0].text})
with open(f"output/g_output_{version}.json","w") as f:
    json.dump(output_lst,f, indent=4, ensure_ascii=False)
