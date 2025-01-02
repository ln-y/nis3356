import asyncio
from openai import AsyncOpenAI
import time
from tqdm import tqdm
import pickle
import yaml, json
import os

base_url = "http://localhost:9077/v1"
api_key = "hereismykey"
from config import model_name
sentiment_choice = ["Appreciation", "Empathy", "Anger", "Skepticism", "Sarcasm", "Objective", "Irrelevant","Advocacy"]
new_sentiment_choice = list(sentiment_choice)
new_sentiment_choice[-1] = "or "+new_sentiment_choice[-1]
sentiment_str = ', '.join(new_sentiment_choice)
print(f"{sentiment_str=}")
prompt = f'''\
Hello AI, I need your assistance in classifying the sentiment of the last comment in a given conversation. Please analyze the dialogue and determine the sentiment expressed in the final comment. The sentiment can be one of the following categories: {sentiment_str}. Here's how you can approach this task:

Read the Conversation: Carefully read through the entire conversation to understand the context and flow of the discussion.
Identify the Last Comment: Locate the last comment made in the conversation.
Analyze the Sentiment: Based on the language used, tone, and context, determine if the sentiment of the last comment is {sentiment_str}.
Consider Context: Keep in mind that the sentiment can be influenced by the preceding comments and the overall conversation.
Classify: Provide a classification for the sentiment of the last comment.
Please remember to focus solely on the last comment for sentiment classification. Here is a sample conversation for you to practice:
'''

async def async_query_openai(tag, query, progress):
    aclient = AsyncOpenAI(
        base_url= base_url,
        api_key= api_key
    )
    completion = await aclient.chat.completions.create(
        model= model_name,
        messages=[
            {"role": "user", "content": f"{prompt}\nClassify the last comment in the following conversation :\n{query}"}
        ],
        extra_body={
            "guided_choice": sentiment_choice
        }
    )
    progress.update(1)
    return tag, completion.choices[0].message.content

async def async_process_queries(queries:dict[str,str], progress):
    tasks = []
    for tagi, qi in tqdm(queries.items(),leave=False,desc="sending"):
        task = asyncio.create_task(async_query_openai(tagi, qi, progress))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main():
    data_flst = os.listdir('data')
    queries = {}
    for fi in data_flst:
        if fi.endswith('.pkl'):
            with open(f"data/{fi}","rb") as f:
                queries_dic = pickle.load(f)
            f_name = fi.split('.')[0]
            for k,v in queries_dic.items():
                queries[f"{f_name}_{k}"] = v
    progress_bar = tqdm(total=len(queries),desc="processing")
    lst = []
    batch_size = 512
    start_time = time.time()
    key_lst = list(queries.keys())
    for i in range(0, len(queries), batch_size):
        batch_queries = {k: queries[k] for k in key_lst[i:i+batch_size]}
        results = await async_process_queries(batch_queries ,progress_bar)
        for tagi, resi in results:
            lst.append({"tag":tagi, "query": queries[tagi], "result": resi})
    with open("1.json","w") as f:
        json.dump(lst,f,ensure_ascii=False,indent=4)
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")
asyncio.run(main())