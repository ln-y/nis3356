import json, pickle
import os
from tqdm import tqdm

from ..util import PostComments, load_post_comments, save_post_comments, CommentInfo, PostCommentsInfo, Comment, view_choice

work_dir = os.path.dirname(__file__)
with open(f"{work_dir}/viewpoint2_.json", "r", encoding="utf-8") as f:
    emotion = json.load(f)

output_dir = f"{work_dir}/out_data_view"

shuiyuan_data_dir = os.path.join(work_dir, "../shuiyuan/data")
bilibili_data_dir = os.path.join(work_dir, "../bilibili/processed_data/comment_pkl")
douyin_data_dir = os.path.join(work_dir, "../douyin/douyin/douyin_list/processed_data_list")

dir_dict = {"shuiyuan": shuiyuan_data_dir,"bilibili": bilibili_data_dir,"douyin": douyin_data_dir}

statistic_dic = {sentiment: 0 for sentiment in view_choice}

for key_dir, dir in dir_dict.items():
    pkl_lst = os.listdir(dir)
    for pkli in tqdm(pkl_lst):
        if pkli.endswith(".pkl"):
            post_comments = load_post_comments(os.path.join(dir, pkli))
            out_comments : PostCommentsInfo = []
            for ind, comment in enumerate(post_comments):
                emotioni = emotion[f"{key_dir}_{pkli.split('.')[0]}_{ind}"]
                out_comments.append(CommentInfo(emotioni, comment))
                statistic_dic[emotioni] += 1
            save_post_comments(f"{output_dir}/{key_dir}_{pkli}", out_comments)
print(statistic_dic)