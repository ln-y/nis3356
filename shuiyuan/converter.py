from dataclasses import dataclass
import pickle
import json
from datetime import datetime

@dataclass
class Comment:
    time: float # timestamp in form of seconds
    content : str
    parent_id: int
    son_ids : list[int]
    likes : int
    
    def __init__(self, created_at, content, parent_id, likes, son_ids=None):
        self.time = created_at
        self.content = content
        self.parent_id = parent_id
        self.likes = likes
        self.son_ids = son_ids if son_ids else []

PostComments = list[Comment]

def load_post_comments(file_path: str) -> PostComments:
    with open(file_path, "rb") as f:
        return pickle.load(f)

def save_post_comments(file_path: str, post_comments: PostComments):
    with open(file_path, "wb") as f:
        pickle.dump(post_comments, f)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def convert(data_list) -> PostComments:
    comment_list = []
    comment_dict = {}
    for data in data_list:
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
        content = data['raw']
        try:
            parent_id = data['reply_to_post_number'] - 1
        except Exception:
            parent_id = None
        likes = data['likes']
        comment = Comment(created_at, content, parent_id, likes)
        comment_list.append(comment)
        comment_dict[len(comment_list) - 1] = comment
    for i, comment in enumerate(comment_list):
        if comment.parent_id is not None:
            parent_comment = comment_dict.get(comment.parent_id)
            if parent_comment:
                parent_comment.son_ids.append(i)
    return comment_list

post_list = [
    {"id": 272450, "reply": 3448},
    {"id": 274039, "reply": 553},
    {"id": 274629, "reply": 24},
    {"id": 274207, "reply": 46},
    {"id": 274872, "reply": 25},
    {"id": 274982, "reply": 15},
    {"id": 275148, "reply": 32},
    {"id": 275120, "reply": 31},
    {"id": 275363, "reply": 14},
    {"id": 275344, "reply": 43},
    {"id": 274643, "reply": 26},
    {"id": 321602, "reply": 370},
    {"id": 276494, "reply": 16},
    {"id": 276994, "reply": 19},
    {"id": 276435, "reply": 54},
    {"id": 277234, "reply": 19},
    {"id": 275098, "reply": 83},
    {"id": 279174, "reply": 91},
    {"id": 295612, "reply": 60},
    {"id": 321620, "reply": 24},
    {"id": 284855, "reply": 50},
    {"id": 276997, "reply": 197},
    {"id": 275154, "reply": 34}
]

def main():
    for post in post_list:
        post_id = post["id"]
        post_data = load_json_file(f'data/{post_id}.json')
        comment_data = convert(post_data)
        save_post_comments(f'data/{post_id}.pkl', comment_data)
        print(f"Successfully converted data from post {post_id} and saved to {post_id}.pkl")

if __name__ == "__main__":
    main()