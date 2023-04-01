import requests
import json
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
#fake_useragent库规避反爬虫
ua = UserAgent()


def download_image(url, filepath):
    try:
        response = requests.get(url, headers={'User-Agent': ua.random}, timeout=10)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"图片下载成功: {filepath}")
    except Exception as e:
        print(f"图片下载失败: {url}, 错误信息: {e}")

#pause_interval暂停时间，max_retry_count失败次数，proxies代理
def baidu_image_crawler(keyword, num_images, max_retry_count=5, pause_interval=60, proxies=None):
    url_template = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={keyword}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word={keyword}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={pn}&rn=30&gsm=1e&1594447993172="

    if not os.path.exists(keyword):
        os.makedirs(keyword)

    count = 0
    success_count = 0
    retry_count = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        while count < num_images:
            pn = count
            url = url_template.format(keyword=keyword, pn=pn)

            try:
                response = requests.get(url, headers={'User-Agent': ua.random}, timeout=10, proxies=proxies)
                response.raise_for_status()
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                retry_count += 1
                if retry_count >= max_retry_count:
                    print(f"暂停 {pause_interval} 秒以规避反爬虫程序")
                    time.sleep(pause_interval)
                    retry_count = 0
                continue
            except requests.exceptions.RequestException as e:
                print(f"请求错误: {e}")
                retry_count += 1
                if retry_count >= max_retry_count:
                    print(f"暂停 {pause_interval} 秒以规避反爬虫程序")
                    time.sleep(pause_interval)
                retry_count = 0
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
    keyword = "猫"#此处更改关键词
    num_images = 10000#此处更改参数
    baidu_image_crawler(keyword, num_images)

