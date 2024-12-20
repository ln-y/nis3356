import json
import pandas as pd
import pickle
import os
from dataclasses import dataclass


@dataclass
class Comment:
    time: float
    content: str
    parent_id: int
    son_ids: list[int]
    likes: int

    def __init__(self, time, content, parent_id=None, son_ids=None, likes=0):
        self.time = time
        self.content = content
        self.parent_id = parent_id
        self.son_ids = son_ids if son_ids else []
        self.likes = likes


data_folder = r'rawdata/'
output_folder = r'processed_data/'
os.makedirs(output_folder + 'json/', exist_ok=True)
os.makedirs(output_folder + 'pkl/', exist_ok=True)

for filename in os.listdir(data_folder):
    if filename.endswith('.csv'):
        comments = {}
        df = pd.read_csv(os.path.join(data_folder, filename), encoding='utf-8')
        for index, row in df.iterrows():
            id = row['comment_id']
            time = row['create_time']
            content = row['content']
            parent_id = row['parent_comment_id'] if row['parent_comment_id'] != 0 else None
            comments[id] = Comment(time, content, parent_id, [], row['like_count'])
            if parent_id is not None:
                comments[parent_id].son_ids.append(id)

        PostComments = [Comment for _ in range(len(comments))]
        index = 0
        for key, value in comments.items():
            if value.son_ids:
                for son_id in value.son_ids:
                    comments[son_id].parent_id = index
            PostComments[index] = value
            if value.parent_id is not None:
                # print(value.parent_id)
                PostComments[value.parent_id].son_ids.remove(key)
                PostComments[value.parent_id].son_ids.append(index)
            index += 1

        # print(PostComments[0])
        # print(PostComments[1])
        # print(PostComments[2])
        # print("------------------")

        comments = {}
        for index, comment in enumerate(PostComments):
            comments[index] = {
                'time': comment.time,
                'content': comment.content,
                'parent_id': comment.parent_id,
                'son_ids': comment.son_ids,
                'likes': comment.likes
            }

        with open(os.path.join(output_folder + 'json/', filename.replace('.csv', '.json')), 'w', encoding='utf-8') as json_file:
            json.dump(comments, json_file, ensure_ascii=False, indent=4)
        with open(os.path.join(output_folder + 'pkl/', filename.replace('.csv', '.pkl')), 'wb') as pickle_file:
            pickle.dump(comments, pickle_file)
