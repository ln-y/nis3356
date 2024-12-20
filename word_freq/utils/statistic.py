from collections import defaultdict

# 从txt文件读取词频并返回一个字典（默认值为0）
def read_word_counts_from_file(file_path):
    word_counter = defaultdict(int)  # 使用defaultdict，默认值为0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 忽略空行
                # 解析每一行：key: value
                line.replace(':', '：')
                word, count = line.strip().split(':')
                word = word.strip("'")  # 去除引号
                count = int(count.strip())
                word_counter[word] += count  # 如果key相同，value会累加
    return word_counter

# 将合并后的词频统计结果写入文件
def write_word_counts_to_file(word_counts, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for word,count in word_counts.items():
            if word.strip():  # 去除空格或其他无用字符
                f.write(f"'{word}': {count}\n")

# 主函数
def main():
    input_file_path = r'word_freq\bilibili\word_counts.txt'  # 你的输入文件路径
    output_file_path = r'word_freq\merged_word_counts.txt'  # 输出文件路径
    
    # 读取并合并词频
    word_counts = read_word_counts_from_file(input_file_path)
    
    # 输出合并后的词频统计结果到文件
    write_word_counts_to_file(word_counts, output_file_path)
    print(f"词频统计结果已写入文件：{output_file_path}")

if __name__ == "__main__":
    main()
