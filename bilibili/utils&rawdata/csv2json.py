import pandas as pd
import json
import time
import chardet

# 检测文件编码
# 读取 CSV 文件
df = pd.read_csv(r"C:\Users\陈楠\Desktop\result_processed\中专“天才”少女光环破灭，姜萍数学竞赛成绩原系老师提供帮助.csv",encoding="gb18030")

# 创建一个字典来存储评论数据
comments = {}

# 遍历每一行，构建评论数据
for index, row in df.iterrows():
    # 将评论时间转换为时间戳
    timestamp = int(time.mktime(time.strptime(row['回复时间'], "%Y-%m-%d %H:%M:%S")))
    
    # 获取评论内容和点赞数
    content = row['评论内容']
    likes = int(row['点赞数量'])
    
    # 查找父评论索引
    parent_id = None
    if row['被回复用户']:
        # 找到父评论的索引
        parent_row = df[df['用户昵称'] == row['被回复用户']]
        if not parent_row.empty:
            parent_id = int(parent_row.index[0])
    
    # 初始化评论数据
    comments[index] = {
        'time': timestamp,
        'content': content,
        'parent_id': parent_id,
        'son_ids': [],
        'likes': likes
    }

# 添加子评论索引
for index, row in df.iterrows():
    if row['被回复用户']:
        parent_row = df[df['用户昵称'] == row['被回复用户']]
        if not parent_row.empty:
            parent_id = int(parent_row.index[0])
            comments[parent_id]['son_ids'].append(index)

# 转换为 JSON 格式并保存
with open(r"C:\Users\陈楠\Desktop\result_processed\中专“天才”少女光环破灭，姜萍数学竞赛成绩原系老师提供帮助.json", 'w', encoding='utf-8') as json_file:
    json.dump(comments, json_file, ensure_ascii=False, indent=4)

print("评论数据已成功保存为 JSON 格式。")