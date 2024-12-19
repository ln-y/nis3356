import requests
import re
import time
import csv
from fake_useragent import UserAgent

headers = {
    "user-agent": UserAgent().random,
    "cookie": "buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; buvid4=03736BB0-6307-7C6E-118E-16C1EA5F3C5949121-023090912-9N4LkoZIf2wWIk7rSe1H5A%3D%3D; rpdid=|(JJmY)YR~mu0J'u~|lRuRkRY; enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=1047735229; DedeUserID__ckMd5=95dc1cf265c61e94; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; hit-dyn-v2=1; CURRENT_QUALITY=80; fingerprint=e910189b9150e4fdaa4f670399e21086; LIVE_BUVID=AUTO9617262313742487; buvid_fp=e910189b9150e4fdaa4f670399e21086; _uuid=3C4A59103-B423-58AB-1387-449E9F12E7BE20001infoc; buvid3=01358D83-5589-79BB-BFE2-901566A4017D54757infoc; b_nut=1730384854; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ0MzUyNjMsImlhdCI6MTczNDE3NjAwMywicGx0IjotMX0.zMMhotIqfrrK6dD16nArSOfJu63_RzqO0qHELVNMByo; bili_ticket_expires=1734435203; SESSDATA=52f75f8a%2C1749728074%2Cb90e6%2Ac1CjAIPm01petAvB_yfKmZarT2WmL8Fyuiqwp8_8wSWifYJF545Zd2VmAztD0tfGckc-gSVjVKNUZ2eWpsTnJpRVFjX2dLYTB6VmRZRUZWRWZkZUZFdVVOdTF6TC1uWTFRUC1DX1AyTEtDc0hRb0dVWVRtTzc2ckNxV2FXcXRrLWtzTVY0Zno1eHZBIIEC; bili_jct=37344050311e074670b1ae9ce5513309; sid=7k4aosf0; b_lsid=762A78E8_193CE2B604C; bsource=search_google; bp_t_offset_1047735229=1011446454402678784; CURRENT_FNVAL=4048; home_feed_column=4; browser_resolution=718-812"
}


def get_video_id(bv):
    url = f'https://www.bilibili.com/video/{bv}'
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    content = html.text
    aid_regx = '"aid":(.*?),"bvid":"{}"'.format(bv)
    video_aid = re.findall(aid_regx, content)[0]
    return video_aid


def fetch_comment_replies(video_id, comment_id, parent_user_name, max_pages=1000):
    replies = []
    preLen = 0
    for page in range(1, max_pages + 1):
        url = f'https://api.bilibili.com/x/v2/reply/reply?oid={video_id}&type=1&root={comment_id}&ps=10&pn={page}'
        try:
            # 添加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and data.get('data') and 'replies' in data['data']:
                    for reply in data['data']['replies']:
                        reply_info = {
                            '用户昵称': reply['member']['uname'],
                            '评论内容': reply['content']['message'],
                            '被回复用户': parent_user_name,
                            '评论层级': '二级评论',
                            '性别': reply['member']['sex'],
                            '用户当前等级': reply['member']['level_info']['current_level'],
                            '点赞数量': reply['like'],
                            '回复时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(reply['ctime']))
                        }
                        replies.append(reply_info)
                    if preLen == len(replies):
                        break
                    preLen = len(replies)
                else:
                    return replies
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
        # 控制请求频率
        time.sleep(0.2)
    return replies


def fetch_comments(video_id, max_pages=1000):
    comments = []
    last_count = 0
    for page in range(1, max_pages + 1):
        url = f'https://api.bilibili.com/x/v2/reply?pn={page}&type=1&oid={video_id}&sort=2'
        try:
            # 添加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'replies' in data['data']:
                    for comment in data['data']['replies']:
                        comment_info = {
                            '用户昵称': comment['member']['uname'],
                            '评论内容': comment['content']['message'],
                            '被回复用户': '',
                            '评论层级': '一级评论',
                            '性别': comment['member']['sex'],
                            '用户当前等级': comment['member']['level_info']['current_level'],
                            '点赞数量': comment['like'],
                            '回复时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(comment['ctime']))
                        }
                        comments.append(comment_info)
                        replies = fetch_comment_replies(video_id, comment['rpid'], comment['member']['uname'])
                        comments.extend(replies)
                        print(comment_info, replies)
                if last_count == len(comments):
                    break
                last_count = len(comments)
            else:
                break
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
        # 控制请求频率
        time.sleep(0.2)
    return comments


def save_comments_to_csv(comments, video_bv):
    with open(f'./result/{video_bv}.csv', mode='w', encoding='utf-8',
              newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['用户昵称', '性别', '评论内容', '被回复用户', '评论层级', '用户当前等级',
                                            '点赞数量', '回复时间'])
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)


filename = './video_list.csv'

# 打开文件并读取数据
with open(filename, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过第一行（标题行）
    for row in reader:
        video_name = row[0]  # 视频名字
        video_bv = row[1]  # video_bv
        print(f'视频名字: {video_name}, video_bv: {video_bv}')
        aid = get_video_id(video_bv)
        print(f'视频aid: {aid}')
        video_id = aid
        comments = fetch_comments(video_id)
        save_comments_to_csv(comments, video_name)
        print(f'视频{video_name}的评论已保存到{video_name}.csv')
