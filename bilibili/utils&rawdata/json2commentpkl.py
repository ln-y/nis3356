# from dataclasses import dataclass
# import pickle

# @dataclass
# class Comment:
#     time: float # 发布时间(时间戳单位s)
#     content : str # 评论内容
#     parent_id: int # 父评论索引
#     son_ids : list[int] # 子评论索引
#     likes : int # 该评论的点赞数

#     def __str__(self):
#         return f"Comment:\ntime={self.time}\ncontent={self.content}\nparent_id={self.parent_id}\nson_ids={self.son_ids}\nlikes={self.likes}"

# # 每个评论/帖子的所有评论应该被放置在一个列表中。父、子评论索引即为其在该列表中的索引。

    

# if __name__ == "__main__":
#     # please check your data before upload
#     import os
#     work_dir = os.path.dirname(__file__)
#     data_path = os.path.join(work_dir, r"douyin\douyin\processed_data\pkl\7380262636904041768.pkl")
#     check_your_data(data_path)

import json
import pickle
from typing import List

# 定义 Comment 类
class Comment:
    def __init__(self, time: float, content: str, parent_id: int, son_ids: List[int], likes: int):
        self.time = time  # 发布时间（时间戳单位s）
        self.content = content  # 评论内容
        self.parent_id = parent_id  # 父评论索引
        self.son_ids = son_ids  # 子评论索引
        self.likes = likes  # 该评论的点赞数

    def __repr__(self):
        return f"Comment(time={self.time}, content={self.content}, parent_id={self.parent_id}, son_ids={self.son_ids}, likes={self.likes})"


# 读取 JSON 文件
def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# 将 JSON 数据转换为 Comment 对象
def convert_json_to_comments(data: dict) -> List[Comment]:
    comments = []
    for key, value in data.items():
        comment = Comment(
            time=value['time'],
            content=value['content'],
            parent_id=value['parent_id'],
            son_ids=value['son_ids'],
            likes=value['likes']
        )
        comments.append(comment)
    return comments


# 保存为 pkl 文件
def save_to_pkl(data: List[Comment], pkl_file_path: str):
    with open(pkl_file_path, 'wb') as file:
        pickle.dump(data, file)

PostComments = list[Comment]

def load_post_comments(file_path: str) -> PostComments:
    with open(file_path, "rb") as f:
        return pickle.load(f)

# def save_post_comments(file_path: str, post_comments: PostComments):
#     with open(file_path, "wb") as f:
#         pickle.dump(post_comments, f)

def check_your_data(file_path: str):
    post_comments = load_post_comments(file_path)
    assert isinstance(post_comments, list)
    assert isinstance(post_comments[0], Comment)
    print("type check passed!\nyour comments[0] are:")
    print(post_comments[0])

# 主函数
def main():
    # 输入的 JSON 文件路径
    json_file_path = 'bilibili\processed_data\json\中专“天才少女”姜萍阿里数学竞赛未获奖，入围系老师违规提供帮助.json'  # 请根据你的实际文件路径修改
    
    # 输出的 pkl 文件路径
    pkl_file_path = 'bilibili\processed_data\pkl\中专“天才少女”姜萍阿里数学竞赛未获奖，入围系老师违规提供帮助.pkl'  # 保存为 pkl 文件的路径
    
    # 读取 JSON 文件
    data = load_json_file(json_file_path)
    
    # 转换为 Comment 对象列表
    comments = convert_json_to_comments(data)
    
    # 保存为 pkl 文件
    save_to_pkl(comments, pkl_file_path)
    print(f"成功将评论数据保存为 {pkl_file_path}")
    check_your_data(pkl_file_path)


if __name__ == "__main__":
    main()
    

