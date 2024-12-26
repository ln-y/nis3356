from ..util import CommentInfo, view_choice

import pickle
import os

view_choice.remove('无法判断')
work_dir = os.path.dirname(__file__)
file_dir = f"{work_dir}/out_data"
out_data_lst = os.listdir(file_dir)

emotion_topic_dic :dict[str, dict[str,int]]={}
time_gap = 86400*10
time_emotion_dic : dict[str, dict[str, dict[int, int]]] = {} # {platform: {emotion : {time : count}}}
for fi in out_data_lst:
    if fi.endswith(".pkl"):
        platformi = fi.split("_")[0]
        if platformi not in time_emotion_dic.keys():
            time_emotion_dic[platformi] = {i: {} for i in view_choice}
        emotion_topic_dic[fi.split(".")[0]] = {i:0 for i in view_choice}
        now_dic = emotion_topic_dic[fi.split(".")[0]]
        with open(f"{file_dir}/{fi}","rb") as f:
            data : list[CommentInfo]= pickle.load(f)
            for comment in data:
                if comment.viewpoint == "无法判断":
                    continue
                now_dic[comment.viewpoint]+=1
                time_begin_num = int(comment.comments.time/time_gap)*time_gap
                time_emotion_dic[platformi][comment.viewpoint][time_begin_num] = time_emotion_dic[platformi][comment.viewpoint].get(time_begin_num, 0) + 1

time_emotion_dic["total"] = {i: {} for i in view_choice}
for key in time_emotion_dic.keys():
    if key != "total":
        for ki, vi in time_emotion_dic[key].items():
            for ki2, vi2 in vi.items():
                time_emotion_dic["total"][ki][ki2] = time_emotion_dic["total"][ki].get(ki2, 0) + vi2

platform_dic = {}
for ki, vi in emotion_topic_dic.items():
    if ki.split("_")[0] not in platform_dic.keys():
        platform_dic[ki.split("_")[0]] = vi
    else:
        for ki2, vi2 in vi.items():
            platform_dic[ki.split("_")[0]][ki2]+=vi2

print(platform_dic)
for key in platform_dic.keys(): 
    print(time_emotion_dic[key])

import matplotlib.pyplot as plt
import numpy as np
import datetime

plt.rcParams['font.sans-serif'] = ['FangSong']  # 用来正常显示中文标签

def draw_time_chart(data:dict[str, dict[str, dict[int, int]]]):
    for platformi in data.keys():
        min_time = -1
        max_time = -1
        plt.figure(figsize=(10, 6))
        for emotioni in data[platformi].keys():
            time_list = list(data[platformi][emotioni].keys())
            time_list.sort()
            if time_list:
                min_time = min(min_time, time_list[0]) if min_time != -1 else time_list[0]
                max_time = max(max_time, time_list[-1]) if max_time != -1 else time_list[-1]
                count_list = [data[platformi][emotioni][timei] for timei in time_list]
                plt.plot(time_list, count_list, label=emotioni)
        
        plt.title(f"{platformi} 评论观点随时间变化")
        plt.xlabel('时间')
        plt.ylabel('评论数量')
        x_tick_place = [i-time_gap/2 for i in range(min_time, max_time+1, time_gap)]
        x_tick_label = [datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d') for i in x_tick_place]
        plt.xticks(x_tick_place, x_tick_label, rotation=35, fontsize = 8)
        plt.legend()
        plt.savefig(f"{work_dir}/time_view_{platformi}.png", dpi=320)
        plt.cla()

def draw_bar_chart(save_path, data, title, x_label, y_label, x_label_name):
    '''
    示例数据：x对应的的y值总数无需归一化
    x_label = ['人群A', '人群B', '人群C']

    y_label = ['食品', '娱乐', '交通', '通讯']

    data = {
        '人群A': [30, 20, 25, 25],
        '人群B': [20, 25, 30, 25],
        '人群C': [25, 20, 25, 30]
    }
    '''

    # 归一化data
    for ki, vi in data.items():
        totali = sum(vi)
        for i in range(len(vi)):
            data[ki][i] = 100 * data[ki][i] / totali
    

    # 创建堆叠条形图
    plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots()
    bottom = [0] * len(x_label)

    for ind, yi in enumerate(y_label):
        percentages = [data[xi][ind] for xi in x_label]
        ax.bar(x_label, percentages, bottom=bottom, label=yi, width=0.35)
        bottom = [bottom[i] + percentages[i] for i in range(len(x_label))]

    # 设置图表标题和标签
    ax.set_title(title)
    ax.set_ylabel('百分比%')
    ax.set_xlabel(x_label_name)
    ax.set_ylim(0, 100)  # 设置y轴范围

    # 添加图例
    ax.legend()

    # 显示图表
    plt.savefig(save_path,dpi=320)
    plt.cla()

platformname2key_dic = {
    "bilibili": "bilibili",
    "douyin": "抖音",
    "shuiyuan": "水源社区",
    "total": "total"
}
platform_dic["total"] = {i:0 for i in view_choice}
for ki, vi in platform_dic.items():
    for ki2, vi2 in vi.items():
        platform_dic["total"][ki2]+=vi2

paltform_draw_data = {platformname2key_dic[ki]: [vi[i] for i in view_choice] for ki, vi in platform_dic.items()}
draw_bar_chart(f"{work_dir}/platform_bar_view.png", paltform_draw_data, "不同平台观点分布", paltform_draw_data.keys(), view_choice, "平台")
draw_time_chart({platformname2key_dic[ki]: vi for ki, vi in time_emotion_dic.items()})