import requests
import re
import time
import csv
import json
headers = {
    'User-Agent': '使用你自己的user-agent'
}
def fetch_comments(video_oid, max_pages=50):#最大页面数量可调整
    comments = []
    last_count = 0
    for page in range(1, max_pages+1):
        url = f'https://api.bilibili.com/x/v2/reply/main?next={page}&type=1&oid={video_oid}&mode=3'
        try:
            # 添加超时设置
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(page)
                if data['data']['replies'] == None:
                    break
                if data and 'replies' in data['data']:
                    for comment in data['data']['replies']:
                        comment_info = {
                            '评论内容': comment['content']['message']
                        }
                        comments.append(comment_info)
                if last_count == len(comments):
                    break
                last_count = len(comments)
            else:
                break
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            break
        # 控制请求频率
        time.sleep(1)
    return comments
 
def save_comments_to_csv(comments, video_name):
    with open(f'./result/{video_name}.csv', mode='w', encoding='utf-8-sig',
              newline='') as file:
        writer = csv.DictWriter(file,
                                fieldnames=['评论内容'])
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)
 
video_name = '你想要的视频名字'  # 视频名字
video_oid = '视频的BV号'  # video_bv
print(f'视频名字: {video_name}, video_bv: {video_oid}')
comments = fetch_comments(video_oid)
save_comments_to_csv(comments, video_name)# 会将所有评论保存到一个csv文件