from ..util import PostComments, load_post_comments, save_post_comments, Comment

import os
from tqdm import tqdm
import pickle, json

work_dir = os.path.dirname(__file__)
data_dir = os.path.join(work_dir, "data")
os.makedirs(data_dir, exist_ok=True)

def parse_talk(comment_lst: PostComments) -> dict[int, str]:
    talk_dict = {}
    for ind, comment in tqdm(enumerate(comment_lst),total=len(comment_lst),leave=False):
        try:
            if comment.parent_id is None:
                talk_dict[ind] = f"[Conversation]\ncomment{ind}:\"{comment.content}\""
            else:
                talk_dict[ind] = f"{talk_dict[comment.parent_id]}\ncomment{ind}:\"{comment.content}\""
        except:
            breakpoint()
    for key in talk_dict.keys():
        talk_dict[key] = talk_dict[key]+f"\n[Last Comment]\ncomment{key}:\"{comment_lst[int(key)].content}\"\n\nNow, classify the sentiment of last comment."
    return talk_dict

def get_all_talk(comment_lst: PostComments, max_num = 16384) -> list[str]:
    talk_lst = []
    tmp_lst = []
    now_num = 0
    for ind, comment in tqdm(enumerate(comment_lst),total=len(comment_lst),leave=False):
        tmp_lst.append(f"comment{ind}:\"{comment.content}\"")
        now_num += len(tmp_lst[-1])
        if now_num > max_num:
            talk_lst.append("\n".join(tmp_lst))
            now_num = 0
            tmp_lst = []
    return talk_lst

shuiyuan_data_dir = os.path.join(work_dir, "../shuiyuan/data")
bilibili_data_dir = os.path.join(work_dir, "../bilibili/processed_data/comment_pkl")
douyin_data_dir = os.path.join(work_dir, "../douyin/douyin/douyin_list/processed_data_list")

dir_dict = {"shuiyuan": shuiyuan_data_dir,"bilibili": bilibili_data_dir,"douyin": douyin_data_dir}

all_post_str = []
for key_dir, dir in dir_dict.items():
    pkl_lst = os.listdir(dir)
    for pkli in tqdm(pkl_lst):
        if pkli.endswith(".pkl"):
            post_comments = load_post_comments(os.path.join(dir, pkli))
            talk_dic = parse_talk(post_comments)
            with open(f"{data_dir}/{key_dir}_{pkli.split('.')[0]}.pkl","wb") as f:
                pickle.dump(talk_dic, f)
            all_post_str.extend(get_all_talk(post_comments))
    else:
        with open(f"{data_dir}/{key_dir}_{pkli.split('.')[0]}.json","w", encoding='utf-8') as f:
                json.dump(talk_dic, f, indent=4, ensure_ascii=False)

with open(f"{data_dir}/all_post_str.pkl","wb") as f:
    print(len(all_post_str))
    pickle.dump(all_post_str, f)

with open(f"{data_dir}/all_post_str.json","w", encoding='utf-8') as f:
    json.dump(all_post_str, f, indent=4, ensure_ascii=False)