import requests
import json
import time
import os

cookies = {
    'cookieconsent_status': 'dismiss',
    '10.119.9.71:80': '', # Fill your own here
    '_t': '', # Fill your own here
    '_forum_session': '' # Fill your own here
}

class ShuiyuanClient:
    def __init__(self):
        self.base_url = 'https://shuiyuan.sjtu.edu.cn'
        
        self.cookies = {
            'cookieconsent_status': 'dismiss',
            '10.119.9.71:80': '',
            '_t': '',
            '_forum_session': ''
        }
        
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6,zh;q=0.5',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'dnt': '1',
            'host': 'shuiyuan.sjtu.edu.cn',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    def update_cookies(self, cookie_dict):
        self.cookies.update(cookie_dict)

    def fetch_reply(self, post_number, reply_number):
        url = f'{self.base_url}/posts/by_number/{post_number}/{reply_number}.json'
        self.headers['referer'] = f'{self.base_url}/t/topic/{post_number}'

        retry_count = 0
        max_retries = 3
        
        while retry_count < max_retries:
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    cookies=self.cookies
                )
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    retry_count += 1
                    print(f"Rate Limit triggered, retrying in 15 seconds... (Attempt {retry_count}/{max_retries})")
                    time.sleep(15)
                elif e.response.status_code == 404:
                    print(f"Deleted reply: {e}")
                    return None
                elif e.response.status_code == 500:
                    retry_count += 1
                    print(f"Server Error, retrying in 30 seconds... (Attempt {retry_count}/{max_retries})")
                    time.sleep(30)
                else:
                    raise
            
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                return None



    def sanitize_reply(self, reply, original_index):
        try: 
            simplified_reply = {
            "created_at": reply["created_at"],
            "reply_count": reply["reply_count"],
            "reply_to_post_number": reply["reply_to_post_number"],
            "raw": reply["raw"],
            "likes": reply["actions_summary"][0]["count"],
            "original_index": original_index
        }
        except KeyError:
            simplified_reply = {
            "created_at": reply["created_at"],
            "reply_count": reply["reply_count"],
            "raw": reply["raw"],
            "likes": 0,
            "original_index": original_index
        }
        return simplified_reply
    
    def fetch_post(self, post_number, reply_number):
        results = []
        for i in range(1, reply_number + 1):
            reply = self.fetch_reply(post_number, i)
            if reply:
                results.append(self.sanitize_reply(reply, reply_number))
        
        # Create the directory if it doesn't exist
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        file_path = f'{data_dir}/{post_number}.json'
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump(results, file)
        else:
            with open(f'data/{post_number}.json', 'w') as file:
                json.dump(results, file)

post_list = [
    {"id": 272450, "reply": 3448},
    {"id": 274039, "reply": 553},
    {"id": 274629, "reply": 24},
    {"id": 274207, "reply": 46},
    {"id": 274872, "reply": 25},
    {"id": 274982, "reply": 15},
    {"id": 275148, "reply": 32},
    {"id": 275120, "reply": 31},
    {"id": 275363, "reply": 14},
    {"id": 275344, "reply": 43},
    {"id": 274643, "reply": 26},
    {"id": 321602, "reply": 370},
    {"id": 276494, "reply": 16},
    {"id": 276994, "reply": 19},
    {"id": 276435, "reply": 54},
    {"id": 277234, "reply": 19},
    {"id": 275098, "reply": 83},
    {"id": 279174, "reply": 91},
    {"id": 295612, "reply": 60},
    {"id": 321620, "reply": 24},
    {"id": 284855, "reply": 50},
    {"id": 276997, "reply": 197},
    {"id": 275154, "reply": 34}
]

def main():
    client = ShuiyuanClient()
    client.update_cookies(cookies)
    for post in post_list:
        post_number = post["id"]
        reply_number = post["reply"]
        client.fetch_post(post_number, reply_number)
        print(f"Successfully saved data of post {post_number}.")

if __name__ == "__main__":
    main()