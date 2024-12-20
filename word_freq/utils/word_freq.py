import json
import jieba
from collections import Counter

# 从 JSON 文件读取数据
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 定义一个函数来处理并统计词频
def count_words(data):
    word_counter = Counter()
    
    for record in data.values():
        content = record.get('content', '')
        # 使用 jieba 进行分词
        words = jieba.cut(content)  # jieba.cut 返回一个生成器
        # 将分词结果更新到统计器
        word_counter.update(words)
    
    return word_counter

def write_word_counts_to_file(word_counts, output_file_path):
    with open(output_file_path, 'a', encoding='utf-8') as f:
        for word, count in word_counts.items():
            if word.strip():  # 去除空格或其他无用字符
                f.write(f"'{word}': {count}\n")
# 主函数
def main():
    # 假设 JSON 文件名为 'data.json'
    file_path = r'douyin\douyin\processed_data\json\7433045899502193946.json'
    
    # 读取 JSON 数据
    data = load_json_file(file_path)
    
    # 统计词频
    word_counts = count_words(data)
    
    # 输出词频统计结果
    for word, count in word_counts.items():
        if word.strip():  # 去除空格或其他无用字符
            print(f"'{word}': {count}")

    output_file_path = r'word_freq\douyin\word_counts.txt'
    write_word_counts_to_file(word_counts, output_file_path)
    print(f"词频统计结果已写入文件：{output_file_path}")

if __name__ == "__main__":
    main()
