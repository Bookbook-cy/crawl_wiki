import json
import time
import wikipediaapi
import pandas as pd
from crawl import CrawlData
import datetime
import uuid
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed


class CrawlWiki(CrawlData):
    def __init__(self, dataf, key_word, max_threads=10):
        super().__init__(dataf, key_word)
        self.max_threads = max_threads
        self.wiki_instances = {}  # 语言-Wikipedia实例缓存

    def get_wikipedia_data(self, i, table_url):
        """单个 Wikipedia URL 的爬取逻辑"""
        lang = urlparse(table_url).netloc.split('.')[0]

        # 复用或创建 Wikipedia API 实例
        if lang not in self.wiki_instances:
            self.wiki_instances[lang] = wikipediaapi.Wikipedia(language=lang,
                                                               user_agent="MyWikipediaBot/1.0 (myemail@example.com)")
        wiki_wiki = self.wiki_instances[lang]

        # 提取 Wikipedia 页面标题
        page_title = urllib.parse.unquote(urlparse(table_url).path.split('/')[-1])
        page = wiki_wiki.page(page_title)
        name = self.dataf['name'].iloc[i]
        country = self.dataf['country'].iloc[i]

        try:
            tables = pd.read_html(table_url)

            for table in tables:
                if self.key_word in table.iloc[:, 0].values:
                    print(f'已处理 {i + 1}/{len(self.dataf["url"])}')

                    data_dict = dict(zip(table.iloc[:, 0], table.iloc[:, 1]))
                    data_dict.update({
                        'url': table_url,
                        'name': name,
                        'title': page.title,
                        'summary': page.summary,
                        'content': page.text,
                        'country': country,
                        'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    return json.dumps(data_dict, indent=4)
            else:
                print(f'已处理 {i + 1}/{len(self.dataf["url"])}')
                return json.dumps({
                    'name': name,
                    'url': table_url,
                    'title': page.title,
                    'summary': page.summary,
                    'content': page.text,
                    'country': country,
                    'state': self.dataf['name_state'].iloc[i] if 'name_state' in self.dataf.columns else 'N/A',
                    'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }, indent=4)

        except Exception as e:
            print(f'{e} - 处理 {i + 1}/{len(self.dataf["url"])} 失败，但 URL 已保存')
            return json.dumps({
                'name': name,
                'url': table_url,
                'title': page.title,
                'summary': page.summary,
                'content': page.text,
                'country': country,
                'state': self.dataf['name_state'].iloc[i] if 'name_state' in self.dataf.columns else 'N/A',
                'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }, indent=4)

    def crawl_data(self):
        """多线程并发爬取 Wikipedia 数据"""
        # 初始化一个空列表，用于存储爬取到的数据
        df_json_list = []
        # 从类的属性中获取所有需要爬取的Wikipedia页面URL列表
        url_list = self.dataf['url']

        # 使用上下文管理器创建一个线程池，最大线程数由类的属性max_threads指定
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # 启动线程池中的线程，每个线程执行get_wikipedia_data方法，并将索引和URL作为参数传递
            future_to_index = {executor.submit(self.get_wikipedia_data, i, url): i for i, url in enumerate(url_list)}

            # 监听完成的线程，获取线程执行结果
            for future in as_completed(future_to_index):
                try:
                    # 获取线程的返回结果
                    result = future.result()
                    # 如果结果不为空，则将其添加到结果列表中
                    if result:
                        df_json_list.append(result)
                except Exception as e:
                    # 捕获线程执行过程中出现的异常，并打印错误信息
                    print(f"线程错误: {e}")

        # 将爬取到的JSON字符串列表转换为JSON对象列表
        json_list = [json.loads(item) for item in df_json_list]
        # 将JSON对象列表转换为Pandas DataFrame
        dfj = pd.DataFrame(json_list)
        # 打印DataFrame，查看爬取结果
        print(dfj)
        # 返回包含爬取数据的DataFrame
        return dfj


def main():
    """程序入口，执行数据爬取并保存"""
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="请选择一个Excel文件", filetypes=[("Excel文件", "*.xlsx")])

    if not file_path.endswith('.xlsx'):
        print('请选择 Excel 文件')
        return

    print(f"你选择的文件是: {file_path}")

    try:
        dataf = pd.read_excel(file_path)
    except Exception as e:
        print(f"文件加载失败: {e}")
        return

    keywords = input('请输入关键词: ')
    file_name = input('请输入要保存的文件名: ')

    # 创建 CrawlWiki 实例，使用 10 个线程并发爬取
    crawl_wiki = CrawlWiki(dataf, keywords.split(), max_threads=10)
    data = crawl_wiki.crawl_data()
    # 数据处理
    data['ID'] = data.apply(lambda x: uuid.uuid4(), axis=1)
    data = data[['ID'] + ['name'] + [col for col in data.columns if col not in ['ID', 'name']]]
    df_cleaned = data.astype(str).apply(lambda x: x.str.replace(r'\[\d+\]', '', regex=True))
    # 保存数据
    output_path = f'../data/民俗民风/{file_name}.csv'
    df_cleaned.to_csv(output_path, encoding='utf-8', index=False)
    print(f"数据已保存至: {output_path}")


if __name__ == '__main__':
    # 编写一个计时器
    start_time = time.time()
    main()
    # time.sleep(5)
    end_time = time.time()
    print(f"程序运行时间: {round(end_time - start_time, 2)}秒")
