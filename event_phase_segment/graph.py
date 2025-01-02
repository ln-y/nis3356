import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import matplotlib as mpl

def set_chinese_font():
    """设置中文字体"""
    # 优先尝试微软雅黑，如果系统没有则尝试其他中文字体
    chinese_fonts = ['Microsoft YaHei', 'SimHei', 'STXihei', 'WenQuanYi Micro Hei']
    for font in chinese_fonts:
        try:
            mpl.rcParams['font.family'] = font
            # 验证字体是否可用
            plt.figure()
            plt.text(0.5, 0.5, '测试中文', fontsize=12)
            plt.close()
            # print(f"成功使用字体: {font}")
            return True
        except:
            continue
    print("警告：未找到合适的中文字体，可能会显示乱码")
    return False

def parse_week_to_date(week_str):
    """将周字符串转换为该周的开始日期"""
    year, week = week_str.split('-W')
    # 使用ISO周格式进行解析
    first_day = datetime.strptime(f'{year}-W{week}-1', '%Y-W%W-%w')
    return first_day

def load_weekly_stats(filepath):
    """从JSON文件加载周统计数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_weekly_stats(data, title, output):
    """绘制评论数量和点赞数量的可视化图表"""
    # 设置中文字体
    set_chinese_font()
    
def plot_weekly_stats(data, title, output):
    """绘制评论数量和点赞数量的可视化图表"""
    # 设置中文字体
    set_chinese_font()
    
    # 设置全局字体大小
    plt.rcParams['font.size'] = 12
    
    # 只调用一次parse_week_to_date
    week_dates = [(parse_week_to_date(week), stats) for week, stats in data.items()]
    sorted_data = sorted(week_dates, key=lambda x: x[0])
    
    # 直接使用已经转换好的日期
    dates = [date for date, _ in sorted_data]
    comment_counts = [stats['comment_count'] for _, stats in sorted_data]
    likes_counts = [stats['likes'] for _, stats in sorted_data]

    # # 打印日期进行验证
    # for date in dates:
    #     print(f"转换后的日期: {date.strftime('%Y-%m-%d')}")

    # 创建图表
    plt.figure(figsize=(12, 10))

    # 折线图
    plt.subplot(2, 1, 1)
    color_palette = ['#3498db', '#e74c3c']  # 蓝色和红色的柔和版本
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    line1 = ax1.plot(dates, comment_counts, marker='o', color=color_palette[0], label='评论数量')
    line2 = ax2.plot(dates, likes_counts, marker='s', color=color_palette[1], label='点赞数量')
    
    ax1.set_xlabel('日期')
    ax1.set_ylabel('评论数量', color=color_palette[0])
    ax2.set_ylabel('点赞数量', color=color_palette[1])
    
    # # 格式化日期
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    # plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    # plt.gcf().autofmt_xdate()
    
    plt.title(f'{title} - 折线图')
    
    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    plt.legend(lines, labels, loc='best')

    # 柱状图
    plt.subplot(2, 1, 2)
    bar_width = 3  # 柱子宽度

    ax3 = plt.gca()
    ax4 = ax3.twinx()
    
    bar1 = ax3.bar([d.toordinal() for d in dates], comment_counts, 
                   width=bar_width, alpha=0.7, color=color_palette[0], label='评论数量')
    bar2 = ax4.bar([d.toordinal()+bar_width for d in dates], likes_counts, 
                   width=bar_width, alpha=0.7, color=color_palette[1], label='点赞数量')
    
    ax3.set_xlabel('日期')
    ax3.set_ylabel('评论数量', color=color_palette[0])
    ax4.set_ylabel('点赞数量', color=color_palette[1])
    
    # 格式化x轴日期
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    # plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    
    plt.title(f'{title} - 柱状图')
    
    # 合并图例
    bars = [bar1, bar2]
    bar_labels = ['评论数量', '点赞数量']
    plt.legend(bars, bar_labels, loc='best')

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

# 主程序
filepath = 'shuiyuan/weekly_stats.json'
shuiyuan_weekly_stats = load_weekly_stats(filepath)
plot_weekly_stats(shuiyuan_weekly_stats, "水源评论趋势统计", "shuiyuan_weekly_stats.png")

filepath = 'bilibili/weekly_stats.json'
bilibili_weekly_stats = load_weekly_stats(filepath)
plot_weekly_stats(bilibili_weekly_stats, "Bilibili评论趋势统计", "bilibili_weekly_stats.png")

filepath = 'douyin/weekly_stats.json'
douyin_weekly_stats = load_weekly_stats(filepath)
plot_weekly_stats(douyin_weekly_stats, "抖音评论趋势统计", "douyin_weekly_stats.png")