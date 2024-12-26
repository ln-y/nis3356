from dataclasses import dataclass
import pickle

@dataclass
class Comment:
    time: float # 发布时间(时间戳单位s)
    content : str # 评论内容
    parent_id: 'int | None '# 父评论索引
    son_ids : list[int] # 子评论索引
    likes : int # 该评论的点赞数

    def __str__(self):
        return f"Comment:\ntime={self.time}\ncontent={self.content}\nparent_id={self.parent_id}\nson_ids={self.son_ids}\nlikes={self.likes}"

# 每个评论/帖子的所有评论应该被放置在一个列表中。父、子评论索引即为其在该列表中的索引。
PostComments = list[Comment]

@dataclass
class CommentInfo:
    emotion: str
    viewpoint: str
    comments: Comment

sentiment_choice = ["Anger","Sympathy", "Appreciation", "Sadness", "Surprise", "Confusion", "Amusement","Unable to Determine"]
view_choice = ["认可", "质疑", "批判", "反思", "讽刺", "无法判断"]
PostCommentsInfo = list[CommentInfo]

def load_post_comments(file_path: str) -> PostComments:
    with open(file_path, "rb") as f:
        return pickle.load(f)

def save_post_comments(file_path: str, post_comments: PostComments):
    with open(file_path, "wb") as f:
        pickle.dump(post_comments, f)

def check_your_data(file_path: str):
    post_comments = load_post_comments(file_path)
    assert isinstance(post_comments, list)
    assert isinstance(post_comments[0], Comment)
    print("type check passed!\nyour comments[0] are:")
    print(post_comments[0])
    

if __name__ == "__main__":
    # please check your data before upload
    import os
    work_dir = os.path.dirname(__file__)
    data_path = os.path.join(work_dir, r"")
    check_your_data(data_path)