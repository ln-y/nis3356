from dataclasses import dataclass
import pickle

@dataclass
class Comment:
    time: float # 发布时间(时间戳单位s)
    content : str # 评论内容
    parent_id: int # 父评论索引
    son_ids : list[int] # 子评论索引
    likes : int # 该评论的点赞数

# 每个评论/帖子的所有评论应该被放置在一个列表中。父、子评论索引即为其在该列表中的索引。
PostComments = list[Comment]

def load_post_comments(file_path: str) -> PostComments:
    with open(file_path, "rb") as f:
        return pickle.load(f)

def save_post_comments(file_path: str, post_comments: PostComments):
    with open(file_path, "wb") as f:
        pickle.dump(post_comments, f)
