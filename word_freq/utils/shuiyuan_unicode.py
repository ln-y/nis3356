import json
import os
import glob

# 读取 JSON 文件
def load_json_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 将 Unicode 转义序列解码为原始字符
def decode_unicode(data):
    # 使用 unicode_escape 解码，得到正确的中文文本
    if isinstance(data, str):
        return data.encode('utf-8').decode('unicode_escape')
    return data

# 处理单个 JSON 文件并保存到新的文件
def process_single_file(input_file_path: str, output_file_path: str):
    # 加载 JSON 数据
    data = load_json_file(input_file_path)
    
    # 解码 JSON 中的 raw 字段
    if 'raw' in data:
        data['raw'] = decode_unicode(data['raw'])
    
    # 将处理后的数据写入新的 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"处理后的数据已保存至 {output_file_path}")

# 处理目录中的所有 JSON 文件
def process_all_json_files(input_dir: str, output_dir: str):
    # 获取目录下所有的 JSON 文件路径
    json_files = glob.glob(os.path.join(input_dir, '*.json'))
    
    # 遍历每个文件并处理
    for json_file in json_files:
        # 构建输出文件路径
        output_file = os.path.join(output_dir, os.path.basename(json_file))
        
        # 处理单个文件
        process_single_file(json_file, output_file)

# 主函数
def main():
    input_dir = './shuiyuan/data/'  # 输入的 JSON 文件目录
    output_dir = './word_freq/shuiyuan/json/'  # 输出的处理后 JSON 文件目录
    
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        print(f"创建输出目录: {output_dir}")
        os.makedirs(output_dir)
    print(f"输出目录: {output_dir}")
    # 处理所有 JSON 文件
    process_all_json_files(input_dir, output_dir)

if __name__ == "__main__":
    main()
