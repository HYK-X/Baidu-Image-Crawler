import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
#fake_useragent库规避反爬虫
import requests

headers = {
    "User-Agent": "",
    "Referer": "https://image.baidu.com/",
}

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def download_image(url, filepath):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved image: {filepath}")
    except Exception as e:
        print(f"Failed to save image: {filepath}. Error: {e}")

def baidu_image_crawler(keyword, num_images, proxies=None):
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    url_template = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={count}&rn=30&gsm=1e&1594447993172="

    success_count = 0
    count = 0
    max_retry_count = 5
    pause_interval = 300  # 暂停时间（秒）
    retry_count = 0
    executor = ThreadPoolExecutor(max_workers=10)

    while success_count < num_images:
        if retry_count >= max_retry_count:
            print(f"连续失败{max_retry_count}次，暂停{pause_interval}秒")
            time.sleep(pause_interval)
            headers["User-Agent"] = get_random_user_agent()
            retry_count = 0

        url = url_template.format(word=keyword, count=count)
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            retry_count += 1
            time.sleep(random.uniform(1, 3))
            continue
        else:
            retry_count = 0

        for item in data.get("data", []):
            if success_count >= num_images:
                break

            img_url = item.get("thumbURL")
            if img_url:
                filepath = os.path.join(keyword, f"{success_count}.jpg")
                executor.submit(download_image, img_url, filepath)
                success_count += 1

        count += 30
        time.sleep(random.uniform(1, 3))


if __name__ == "__main__":
    keyword = "狗"
    num_images = 100000
    baidu_image_crawler(keyword, num_images)