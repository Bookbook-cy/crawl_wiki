import json
import wikipediaapi
import pandas as pd
from crawl import CrawlData
import datetime
import uuid
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse
import urllib.parse


class CrawlWiki:
    def __init__(self, dataf, key_word, max_threads=10):
        self.max_threads = max_threads
        self.wiki_instances = {}
        self.dataf = dataf
        self.key_word = key_word

    def crawl_data(self):

        df_json_list = []
        # 遍历每个网址以获取并处理表格数据

        url_list = self.dataf['url']
        for i, table_url in enumerate(url_list):
            lang = urlparse(url_list[i]).netloc.split('.')[0]

            if lang not in self.wiki_instances:
                self.wiki_instances[lang] = wikipediaapi.Wikipedia(language=lang,
                                                                   user_agent="MyWikipediaBot/1.0 (myemail@example.com)")
            wiki_wiki = self.wiki_instances[lang]

            page = wiki_wiki.page(urllib.parse.unquote(self.dataf['url'].iloc[i].split('/')[-1]))
            name = self.dataf['name'].iloc[i]
            country = self.dataf['country'].iloc[i]

            try:
                # 从网址中读取HTML表格数据
                tables = pd.read_html(table_url)

                # 选取表格中有Service type 关键字的表格
                for table in tables:
                    # 如果关键词在表格中存在，则进行后续处理
                    if self.key_word in table.iloc[:, 0].values:
                        # 打印当前网址处理进度

                        print(f'已经处理完成{i + 1}/{len(url_list)}')

                        # 将表格数据转换为字典格式
                        data_dict = dict(zip(table.iloc[:, 0], table.iloc[:, 1]))
                        data_dict['url'] = table_url
                        data_dict['name'] = name
                        data_dict['title'] = page.title
                        data_dict['summary'] = page.summary
                        data_dict['content'] = page.text
                        data_dict['country'] = country
                        data_dict['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        df_json_list.append(json.dumps(data_dict, indent=4))
                        # 打印当前收集到的JSON数据列表
                        # print(df_json_list)
                        # 如果关键词不在表格中，则将该网址添加到列表中
                        break
                else:
                    print(f'已经处理完成{i + 1}/{len(url_list)}')
                    json_data = json.dumps({
                        'name': name,
                        'url': table_url,
                        'title': page.title,
                        'summary': page.summary,
                        'content': page.text,
                        'country': country,
                        'state': self.dataf['name_state'].iloc[i] if 'name_state' in self.dataf.columns else 'N/A',
                        'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                        indent=4)
                    df_json_list.append(json_data)

            except Exception as e:
                # 打印异常信息
                # print(f'第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')
                json_data = json.dumps({
                    'name': name,
                    'url': table_url,
                    'title': page.title,
                    'summary': page.summary,
                    'content': page.text,
                    'country': country,
                    'state': self.dataf['name_state'].iloc[i] if 'name_state' in self.dataf.columns else 'N/A',
                    'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                    indent=4)
                df_json_list.append(json_data)
                print(f'{e}，但是url已保存，已经处理完成{i + 1}/{len(url_list)}')

        # 将JSON字符串列表转换回字典列表
        json_list = [json.loads(item) for item in df_json_list]
        # 将字典列表转换为DataFrame格式
        dfj = pd.DataFrame(json_list)
        # 打印最终的DataFrame数据
        print(dfj)
        return dfj


def run():
    # 创建Tkinter根窗口并隐藏，防止额外窗口弹出
    root = tk.Tk()
    root.withdraw()

    # 使用文件对话框让用户选择文件，仅显示所有文件类型
    file_path = filedialog.askopenfilename(title="请选择一个文件",
                                           filetypes=[("所有文件", "*.*")])
    if file_path.endswith('.xlsx'):
        dataf = pd.read_excel(file_path)
    else:
        print('请选择Excel文件')
        exit()
    # 输出用户选择的文件路径
    print(f"你选择的文件是: {file_path}")

    # 初始化WikipediaAPI对象，设置语言为英语和自定义的User-Agent

    # 读取用户选择的Excel文件到DataFrame

    # 提示用户输入关键词
    keywords = input('请输入关键词: ')
    file_name = input('请输入文件名')
    # 创建CrawlWiki实例，传入DataFrame和关键词
    crawl_wiki = CrawlWiki(dataf, keywords.split())

    # 调用实例方法获取爬取的数据
    data = crawl_wiki.crawl_data()
    # 为每行数据生成唯一的ID
    data['ID'] = data.apply(lambda x: uuid.uuid4(), axis=1)
    # 将ID列移到第一列
    data = data[['ID'] + ['name'] + [col for col in data.columns if col != 'ID' and col != 'name']]
    # 清洗数据，移除文本中的引用标记
    df_cleaned = data.astype(str).apply(lambda x: x.str.replace(r'\[\d+\]', '', regex=True))

    # 将处理后的数据保存到新的Excel文件
    df_cleaned.to_csv(f'../data/民俗民风/{file_name}.csv', encoding='utf-8', index=False)
    # df_cleaned.to_excel('../data/india_festival_info.xlsx', index=False)


if __name__ == '__main__':
    run()
