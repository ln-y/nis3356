import json, pickle
import os
from tqdm import tqdm

from ..util import PostComments, load_post_comments, save_post_comments, CommentInfo, PostCommentsInfo, Comment, sentiment_choice, view_choice, targets_choice

work_dir = os.path.dirname(__file__)
with open(f"{work_dir}/emotion_new_cache10.json", "r", encoding="utf-8") as f:
    emotion = json.load(f)
with open(f"{work_dir}/viewpoint3.json", "r", encoding="utf-8") as f:
    views = json.load(f)
with open(f"{work_dir}/target0.json", "r", encoding="utf-8") as f:
    targets = json.load(f)

output_dir = f"{work_dir}/out_data"

shuiyuan_data_dir = os.path.join(work_dir, "../shuiyuan/data")
bilibili_data_dir = os.path.join(work_dir, "../bilibili/processed_data/comment_pkl")
douyin_data_dir = os.path.join(work_dir, "../douyin/douyin/douyin_list/processed_data_list")

dir_dict = {"shuiyuan": shuiyuan_data_dir,"bilibili": bilibili_data_dir,"douyin": douyin_data_dir}

statistic_dic = {sentiment: 0 for sentiment in sentiment_choice}
view_staticic_dic = {view: 0 for view in view_choice}
target_staticic_dic = {target: 0 for target in targets_choice}
for key_dir, dir in dir_dict.items():
    pkl_lst = os.listdir(dir)
    for pkli in tqdm(pkl_lst):
        if pkli.endswith(".pkl"):
            post_comments = load_post_comments(os.path.join(dir, pkli))
            out_comments : PostCommentsInfo = []
            for ind, comment in enumerate(post_comments):
                key = f"{key_dir}_{pkli.split('.')[0]}_{ind}"
                emotioni = emotion[key]
                viewi = views[key]
                targeti = targets[key]
                out_comments.append(CommentInfo(emotioni, viewi, targeti, comment))
                statistic_dic[emotioni] += 1
                view_staticic_dic[viewi] += 1
                target_staticic_dic[targeti] += 1
            save_post_comments(f"{output_dir}/{key_dir}_{pkli}", out_comments)
print(statistic_dic)
print(view_staticic_dic)
print(target_staticic_dic)