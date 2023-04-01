import os
import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import JSONDecodeError

def download_image(img_url, file_path, headers):
    try:
        img_data = requests.get(img_url, headers=headers).content
        with open(file_path, "wb") as f:
            f.write(img_data)
            print(f"图片保存成功: {file_path}")
            return True
    except:
        print(f"图片保存失败: {file_path}")
        return False
#max_workers为线程数，pause_interval暂停时间，max_retry_count失败次数
def baidu_image_crawler(keyword, num_images, max_workers=16, pause_interval=60, max_retry_count=3):
    url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word={keyword}"
    #请求user_agents规避反爬虫
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    ]

    if not os.path.exists(keyword):
        os.mkdir(keyword)

    count = 0
    retry_count = 0
    while count < num_images:
        headers = {"User-Agent": random.choice(user_agents)}

        try:
            response = requests.get(f"{url}&pn={count}", headers=headers)
            data = response.json()
        except JSONDecodeError:
            print("JSON 解析错误，跳过当前请求")

            retry_count += 1
            if retry_count >= max_retry_count:
                print(f"暂停 {pause_interval} 秒以规避反爬虫程序")
                time.sleep(pause_interval)
                retry_count = 0
            continue

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            success_count = 0
            for img_info in data.get("data", []):
                img_url = img_info.get("thumbURL")
                if img_url:
                    file_path = os.path.join(keyword, f"{count}.jpg")
                    result = executor.submit(download_image, img_url, file_path, headers)
                    if result.result():
                        success_count += 1
                        count += 1

                if count >= num_images:
                    break

            if success_count == 0:
                retry_count += 1
                if retry_count >= max_retry_count:
                    print(f"暂停 {pause_interval} 秒以规避反爬虫程序")
                    time.sleep(pause_interval)
                    retry_count = 0
                else:
                    retry_count = 0

if __name__ == "__main__":
    keyword = "手机"#此处更改关键词
    num_images = 10000#此处更改参数
    baidu_image_crawler(keyword, num_images)
