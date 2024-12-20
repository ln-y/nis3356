import pickle
import json
from dataclasses import dataclass

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
# 从 pkl 文件加载数据
def load_pkl_file(pkl_file_path):
    with open(pkl_file_path, 'rb') as f:
        data = pickle.load(f)
    return data

# 将数据保存为 json 文件
def save_as_json(data, json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 主函数
def main():
    pkl_file_path = r'shuiyuan\data\272450.pkl'  # 你的 pkl 文件路径
    json_file_path = r'shuiyuan\json\converted_file.json'  # 目标 json 文件路径
    
    # 加载 pkl 数据
    data = load_pkl_file(pkl_file_path)
    
    # 将数据保存为 json 文件
    save_as_json(data, json_file_path)
    print(f"已成功将 pkl 文件转换为 json 文件：{json_file_path}")

if __name__ == "__main__":
    main()
