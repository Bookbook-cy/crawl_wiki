import pandas as pd
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm

# 读取包含网址的 CSV 文件（假设网址存储在 'url' 列中）
input_file = '../data/tiktok.xlsx'  # 替换为你的文件名
df = pd.read_excel(input_file, sheet_name='Sheet2')

# 创建一个字典用于存储网址和源码
results = []

# 遍历网址列表
# url = df["链接地址"]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def get_tiktok(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return {
            "url": url,
            "id": re.search(r'(?<="uniqueId":")(.+?)(?=",)', response.text).group(),
            "UID": re.search(r'(?<=\{"user":\{"id":")(.+?)(?=")', response.text).group(),
            "name": re.search(r'(?<=nickname":")(.+?)(?=")', response.text).group()
        }

    except Exception as e:
        print(f"获取失败: {url} - {e}")
        return {
            "url": url,
            "id": 'NaN',
            "UID": 'NaN',
            "name": 'NaN'
        }


def get_facebook(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")  # 禁止图片
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        # 给页面点时间加载
        #  time.sleep(3)
        html_source = driver.page_source

        # 提取信息（你可以根据页面结构再微调）
        return {
            "url": url,
            "id": re.search(r'(?<=<title>)(.+?)(?= \| )', html_source).group() if re.search(
                r'(?<=<title>)(.+?)(?= \| )', html_source) else '',
            "UID": re.search(r'(?<=userVanity":")(.+?)(?=")', html_source).group() if re.search(
                r'(?<=userVanity":")(.+?)(?=")', html_source) else '',
            "name": re.search(r'(?<=fb://profile/)(.+?)(?=")', html_source).group() if re.search(
                r'(?<=fb://profile/)(.+?)(?=")', html_source) else ''
        }
    except Exception as e:
        print(f"获取失败: {url} - {e}")
        return {
            "url": url,
            "id": '',
            "UID": '',
            "name": ''
        }
    finally:
        try:
            driver.quit()
        except:
            pass


def face(url):
    with ThreadPoolExecutor(max_workers=5) as executor:  # Facebook 页面重，建议少点线程
        results = list(tqdm(executor.map(get_facebook, url), total=len(url)))

    # 打印进度（可选）
    for i, r in enumerate(results, 1):
        print(f"[{i}/{len(results)}] 获取完成: {r['url']}")

    # 保存到 Excel
    df_result = pd.DataFrame(results)
    df_result.to_excel("../data/facebook结果_顺序保留.xlsx", index=False)
    print("✅ Facebook 数据已保存到 facebook结果_顺序保留.xlsx")


def tiktok(url):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_tiktok, url))  # 顺序保持！

    # 打印进度（可选）
    for i, r in enumerate(results, 1):
        print(f"[{i}/{len(results)}] 获取完成: {r['url']}")

    # 保存
    df_result = pd.DataFrame(results)
    df_result.to_excel("tiktok结果_顺序保留.xlsx", index=False)
    t2 = time.time()
    print("✅ 已保存为 tiktok结果_顺序保留.xlsx")
    print(df_result)


if __name__ == '__main__':
    t2 = time.time()
