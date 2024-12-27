from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib as mpl
import os, sys, platform

def get_system_font():
    """获取系统中文字体路径"""
    system = sys.platform
    if system == 'win32':
        # Windows系统常见中文字体路径
        font_paths = [
            r"C:\Windows\Fonts\simhei.ttf",  # 黑体
            r"C:\Windows\Fonts\msyh.ttf",    # 微软雅黑
            r"C:\Windows\Fonts\simsun.ttc",  # 宋体
        ]
    elif system == 'darwin':
        # macOS系统常见中文字体路径
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
        ]
    else:
        # Linux系统常见中文字体路径
        font_paths = [
            "/usr/share/fonts/wenquanyi/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ]

    # 检查字体文件是否存在
    for font_path in font_paths:
        if os.path.exists(font_path):
            # print(f"使用字体: {font_path}")
            return font_path
    
    raise FileNotFoundError("未找到可用的中文字体文件")

def set_chinese_font():
    """设置中文字体"""
    chinese_fonts = ['Microsoft YaHei', 'SimHei', 'STXihei', 'WenQuanYi Micro Hei']
    for font in chinese_fonts:
        try:
            mpl.rcParams['font.family'] = font
            plt.figure()
            plt.text(0.5, 0.5, '测试中文', fontsize=12)
            plt.close()
            # print(f"成功使用字体: {font}")
            return font
        except:
            continue
    print("警告：未找到合适的中文字体，可能会显示乱码")
    return 'SimHei'  # 默认返回黑体

def load_word_frequencies(file_path, stopwords):
    """从文件加载词频数据"""
    word_freq = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 处理每一行，去除引号和空格
                line = line.strip().replace("'", "")
                if line:
                    word, freq = line.split(':')
                    if word.strip() not in stopwords:
                        word_freq[word.strip()] = int(freq.strip())
        return word_freq
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return {}

def generate_wordcloud(word_freq, stopwords, output_path):
    """生成词云图"""
    # 获取中文字体
    font_path = get_system_font()
    
    # 创建词云对象
    wc = WordCloud(
        font_path=font_path,  # 中文字体路径
        width=1200,           # 宽度
        height=800,           # 高度
        background_color='white',  # 背景颜色
        max_words=200,        # 最大显示词数
        max_font_size=150,    # 最大字体大小
        min_font_size=10,     # 最小字体大小
        random_state=42,      # 随机状态，保证可重复性
        stopwords=stopwords,  # 停用词集合
        colormap='viridis'    # 色彩方案
    )
    
    # 生成词云
    wc.generate_from_frequencies(word_freq)
    
    # 显示词云图
    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    
    # 保存图片
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"词云图已保存至: {output_path}")

def graph(input_file, output_file):
    # 定义停用词
    stopwords = {
        '回复', '的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '和', '与', '这', '那',
        '都', '也', '就', '要', '而', '但', '又', '或', '如果', '因为', '所以', '可以', '能', '会',
        '到', '为', '及', '等', '着', '说', '从', '向', '给', '但是', '然后', '因此', '于是', '所以',
        '只是', '不过', '并且', '而且', '，', '[', ':', ']', '"', '(', ')', 'upload', 'topic', 'jpeg',
        'Screenshot', '272450', 'username', 'zhihu', '!', 'post', 'quote', 'username', '!', '！', '、',
        '，', '。', ',', '.', ':', '?', '？', '$', '（', '）', '：', 'https', '*', '“', '”', '<', '>', '|',
        '…', '1', 'https', '/', '-', 'div', 'png', 'image', 'com', '2024', 'tieba', '2', '哔哩', '=', '{',
        '}', '@', '吗', '自己', '12', '《', '》', '人家', '这个', 'details', '一个', '一点', '就是', '不', '有',
        'details', '应该', '有', 'with', '将', '这些', '那些', '这么', '那么', '这种', '那种', '这样', '那样',
        '没有', 'IMG', '\\', '他们', '是', '不是', '是不是', '被', '我们', '你们', 'cn', 'www', '&', '一', '+',
        '3', '人', '对', '还', '会', '不会', '图片', '吧'
        # 可以根据需要添加更多停用词
    }
    
    # 加载词频数据
    word_freq = load_word_frequencies(input_file, stopwords)
    
    if word_freq:
        # 生成词云
        generate_wordcloud(word_freq, stopwords, output_file)
    else:
        print("未能成功加载词频数据")

if __name__ == "__main__":
    platform_list = ['bilibili', 'douyin', 'shuiyuan']
    for platform in platform_list:
        input_file_path = f'{platform}/top_k.txt'
        output_file_path = f'{platform}_wordcloud.png'
        graph(input_file_path, output_file_path)
