from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

import os
import tqdm
import pickle, json

version = 10
from config import model_name
sentiment_choice = ["Anger","Sympathy", "Appreciation", "Sadness", "Surprise", "Confusion", "Amusement","Unable to Determine"]
new_sentiment_choice = list(sentiment_choice)
new_sentiment_choice[-1] = "or "+new_sentiment_choice[-1]
sentiment_str = ', '.join(new_sentiment_choice)
print(f"{sentiment_str=}")
prompt = f'''\
**Task Description:**
You will be presented with a series of comments that form a conversation. Your task is to analyze the final comment in each sequence and categorize it into one of the following emotional categories: {sentiment_str}. Ensure that your classification is as accurate as possible and select only the category that best fits the sentiment expressed in the last comment. If the sentiment is not clear or cannot be confidently classified into any of the provided categories, choose "Unable to Determine".

**Input Format:**
- Conversations will be provided as a sequence of comments, with each comment in a new line.
- The last comment in the sequence is the one you need to classify.

**Output Format:**
- For each conversation, output a single emotional category label that matches one of the following: {sentiment_str}.

**Example:**

1.
[Conversation]
comment146:"这件事要是自媒体主播炒作起来的又会如何?轮到你自己就准备无事发生?"
[Last Comment]
comment146:"这件事要是自媒体主播炒作起来的又会如何?轮到你自己就准备无事发生?"

Classification: Anger

2.
[Conversation]
comment32:"真的感慨，要是考上国内高中那天才就被埋没了，幸好上了专"
[Last Comment]
comment32:"真的感慨，要是考上国内高中那天才就被埋没了，幸好上了专"

Classification: Sympathy

3.
[Conversation]
comment48:"致敬每一个有所热爱的人"
[Last Comment]
comment48:"致敬每一个有所热爱的人"

Classification: Appreciation

4.
[Conversation]
comment117:"哎，突然想起来清北强基面试的时候，问我憧憬的大学生活是什么样的，我说可以一心研究数学，不用学语文什么我不想学的，他们和我说，可能你想得太美好了。。。"
[Last Comment]
comment117:"哎，突然想起来清北强基面试的时候，问我憧憬的大学生活是什么样的，我说可以一心研究数学，不用学语文什么我不想学的，他们和我说，可能你想得太美好了。。。"

Classification: Sadness

5.
[Conversation]
comment82:"这是真牛逼，今天刷到都惊了"
[Last Comment]
comment82:"这是真牛逼，今天刷到都惊了"

Classification: Surprise

6.
[Conversation]
comment45:"我感觉有点丁真🤔没经过系统训练能到这种水平吗，我认识的IMO金牌都没考到她这个排名，这种天赋之前没人发掘吗🤔"
[Last Comment]
comment45:"我感觉有点丁真🤔没经过系统训练能到这种水平吗，我认识的IMO金牌都没考到她这个排名，这种天赋之前没人发掘吗🤔"

Classification: Confusion

7.
[Conversation]
comment1929:"这只是国家对姜萍的保护罢了，姜萍现在已经在研究1nm芯片了，加油姜萍，我们相信你[笑哭]"
comment1930:"JP已经在和三体人沟通了[笑哭]"
[Last Comment]
comment1930:"JP已经在和三体人沟通了[笑哭]"

Classification: Amusement

8.
[Conversation]
comment1693:"呵呵"
[Last Comment]
comment1693:"呵呵"

Classification: Unable to Determine

**Start Task:**

[[CONTENT]]

Classification: 
'''

guided_decoding_params = GuidedDecodingParams(choice=sentiment_choice)
sampling_params = SamplingParams(temperature=0.8, top_p=0.95, guided_decoding=guided_decoding_params) # 

llm = LLM(model = model_name, gpu_memory_utilization= 0.95, enforce_eager=True, max_num_seqs= 128, enable_prefix_caching=True)

data_flst = os.listdir('data')
tag_lst = []
prompt_lst = []
for fi in data_flst:
    if fi.endswith('.pkl'):
        with open(f"data/{fi}","rb") as f:
            queries_dic = pickle.load(f)
        f_name = fi.split('.')[0]
        for k,v in queries_dic.items():
            tag_lst.append(f"{f_name}_{k}")
            prompt_lst.append(prompt.replace("[[CONTENT]]", v.replace('\nNow, classify the sentiment of last comment.','')))
# progress_bar = tqdm(total=len(queries),desc="processing")
print(len(tag_lst))
with open(f"v{version}.log","w") as f:
    f.write(str(len(tag_lst))+"\n")
    f.write(prompt_lst[0]+"\n\n")
    f.write(prompt_lst[512]+"\n\n")
    f.write(prompt_lst[2048]+"\n\n")

llm.generate(prompts=prompt_lst[0], sampling_params=sampling_params)
outputs = llm.generate(prompts=prompt_lst, sampling_params=sampling_params)

output_lst = []
for ind, outputi in enumerate(outputs):
    output_lst.append({"tag":tag_lst[ind], "prompt": prompt_lst[ind], "output": outputi.outputs[0].text})
with open(f"output/output_new{version}.json","w") as f:
    json.dump(output_lst,f, indent=4, ensure_ascii=False)
