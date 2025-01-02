from vllm import LLM, SamplingParams

import os
import tqdm
import pickle, json

version = 0
prompt = '''
Please review the following discussion from a comment section and extract the main viewpoints. Each viewpoint summary should begin with a keyword, followed by an elaboration of the point. Ensure that the summaries accurately reflect the core content of the discussion and that each point is clear and concise.

'''

from config import model_name
work_dir = os.path.dirname(__file__)

with open(f"{work_dir}/all_post_str.pkl","rb") as f:
    all_post_lst = pickle.load(f)

prompt_lst = [prompt + post for post in all_post_lst]

with open(f"abv{version}.log","w") as f:
    f.write(prompt[0]+"\n\n"+prompt[10])

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=32768, repetition_penalty=1.2, seed=42) # 

llm = LLM(model = model_name, gpu_memory_utilization= 0.95, enforce_eager=True, max_num_seqs= 16)



outputs = llm.generate(prompts=prompt_lst, sampling_params=sampling_params)

output_lst = []
for ind, outputi in enumerate(outputs):
    output_lst.append({"prompt": prompt_lst[ind], "output": outputi.outputs[0].text})
print(output_lst)
with open(f"output/abstract_{version}.json","w") as f:
    json.dump(output_lst,f, indent=4, ensure_ascii=False)