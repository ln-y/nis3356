from vllm import LLM, SamplingParams

import os
import tqdm
import pickle, json
import logging

version = 0
prompt = '''
**Emotion Type Identification Task**

**Task Description:**
Please identify and list the different types of emotions present in the following comment section discussions. Your goal is to recognize and categorize the distinct emotional types without detailed sentiment analysis.

**Input Data:**
[[ Input Data ]]

**Output Requirements:**
1. List all distinct emotional types present in the comments.
2. Detailed analysis of each comment is not required; only the identification of emotional types is needed.

**Guidelines for Analysis:**
- Quickly scan the comment content to identify keywords or phrases that express emotions.
- Based on the emotional vocabulary or expressions, categorize the different emotional types.
- Ignore the intensity and specific details of the emotions, focusing only on the types of emotions.

**Example Output:**
- Appreciation
- Sympathy
- Anger
- Joy
- Sadness
- Surprise
- Fear

**Notes:**
- Ensure to cover all different emotional types, even if some appear only once.
- If comments contain mixed emotions, they should also be identified and listed.
'''

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                    ])

from config import model_name
work_dir = os.path.dirname(__file__)

with open(f"{work_dir}/all_post_str.pkl","rb") as f:
    all_post_lst = pickle.load(f)

prompt_lst = [prompt.replace("[[ Input Data ]]", post) for post in all_post_lst]

# with open(f"abv{version}.log","w") as f:
#     f.write(prompt[0]+"\n\n"+prompt[10])

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=16384, repetition_penalty=1.2, seed=42) # 

llm = LLM(model = model_name, gpu_memory_utilization= 0.95, enforce_eager=True, max_num_seqs= 24)



outputs = llm.generate(prompts=prompt_lst, sampling_params=sampling_params)

output_lst = []
for ind, outputi in enumerate(outputs):
    output_lst.append({"prompt": prompt_lst[ind], "output": outputi.outputs[0].text})
    logger.info(f"Output {ind} generated:\n{outputi.outputs[0].text}\n")

with open(f"output/abstract_em_{version}.json","w") as f:
    json.dump(output_lst,f, indent=4, ensure_ascii=False)