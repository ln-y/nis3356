import json
import pickle
import os

# 定义输入和输出目录
input_dir = r'C:\Users\陈楠\Desktop\result_processed'  # JSON 文件所在目录
output_dir = r'C:\Users\陈楠\Desktop\result_processed\pickle'  # Pickle 文件保存目录

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历输入目录中的所有 JSON 文件
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_dir, filename)
        
        # 从 JSON 文件读取数据
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # 生成对应的 Pickle 文件名
        pickle_filename = filename.replace('.json', '.pickle')
        pickle_file_path = os.path.join(output_dir, pickle_filename)
        
        # 将数据写入 Pickle 文件
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)

        print(f"{filename} 已成功转换为 {pickle_filename}")

print("所有 JSON 文件已成功转换为 Pickle 文件。")