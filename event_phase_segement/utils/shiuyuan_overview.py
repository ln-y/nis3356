import json
import os
from datetime import datetime
from collections import defaultdict

# 处理单个 JSON 文件
def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    weekly_stats = defaultdict(lambda: {'comment_count': 0, 'likes': 0, 'comments': []})
    
    for comment in data:
        created_at = comment.get('created_at')
        likes = comment.get('likes', 0)
        raw_comment = comment.get('raw', "")
        
        # 转换 created_at 为 datetime 对象
        comment_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        year, week, _ = comment_time.isocalendar()  # 获取年和周数
        week_key = f"{year}-W{week:02d}"
        
        # 更新统计数据
        weekly_stats[week_key]['comment_count'] += 1
        weekly_stats[week_key]['likes'] += likes
        weekly_stats[week_key]['comments'].append({
            'raw': raw_comment,
            'likes': likes,
            'created_at': created_at
        })
    
    return weekly_stats

# 处理目录下所有的 JSON 文件
def process_all_files(directory):
    all_weekly_stats = defaultdict(lambda: {'comment_count': 0, 'likes': 0, 'comments': []})
    
    # 遍历目录中的所有 JSON 文件
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            weekly_stats = process_json_file(file_path)
            
            # 合并统计结果
            for week_key, stats in weekly_stats.items():
                all_weekly_stats[week_key]['comment_count'] += stats['comment_count']
                all_weekly_stats[week_key]['likes'] += stats['likes']
                all_weekly_stats[week_key]['comments'].extend(stats['comments'])
    
    return all_weekly_stats

# 保存每周统计结果为 JSON 文件
def save_weekly_stats_to_json(weekly_stats, output_directory):
    for week_key, stats in weekly_stats.items():
        # 保存每周的统计数据
        output_file_path = os.path.join(output_directory, f"{week_key}.json")
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)

# 保存总的周统计结果为一个总 JSON 文件
def save_stats_to_json(weekly_stats, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(weekly_stats, f, ensure_ascii=False, indent=4)

# 主函数
def main(input_directory, output_directory, overview_file_path):
    # 处理所有文件
    weekly_stats = process_all_files(input_directory)
    
    # 保存每周详细评论数据
    save_weekly_stats_to_json(weekly_stats, output_directory)
    
    # 保存总览统计数据
    save_stats_to_json(weekly_stats, overview_file_path)

# 执行
if __name__ == "__main__":
    input_directory = r"word_freq\shuiyuan\json"  # 指定存放 JSON 文件的目录
    output_directory = r"event_phase_segement\shuiyuan\weekly_details"  # 每周评论的 JSON 文件存放目录
    overview_file_path = r"event_phase_segement\shuiyuan\weekly_overview.json"  # 总览统计结果文件路径
    main(input_directory, output_directory, overview_file_path)
