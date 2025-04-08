import pandas as pd
import json

# 读取Excel文件中的铁路列表数据
# df = pd.read_excel('../data_source/japan_bus.xlsx')

# 提取网址列
# url = df['url']

# 初始化一个空列表用于存储转换后的JSON数据
df_json_list = []


class CrawlData:

    def __init__(self, dataf, key_word):
        self.dataf = dataf
        self.key_word = key_word

    # 处理网站列表爬取信息
    def crawl_data(self):
        # 遍历每个网址以获取并处理表格数据

        url_list = self.dataf['url']
        for i, table_url in enumerate(url_list.iloc[1:5]):
            try:
                # 从网址中读取HTML表格数据
                tables = pd.read_html(table_url)
                # 选取表格中有Service type 关键字的表格
                for table in tables:
                    # 如果关键词在表格中存在，则进行后续处理
                    if self.key_word in table.iloc[:, 0].values:
                        # 打印当前网址处理进度

                        print(f'第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')

                        # 将表格数据转换为字典格式
                        data_dict = dict(zip(table.iloc[:, 0], table.iloc[:, 1]))
                        # 将网址添加在列表中
                        data_dict['url'] = table_url

                        # 将字典数据转换为 JSON 格式
                        json_data = json.dumps(data_dict, indent=4)
                        # 将JSON数据添加到列表中
                        df_json_list.append(json_data)
                        # 打印当前收集到的JSON数据列表
                        # print(df_json_list)
                    # 如果关键词不在表格中，则将该网址添加到列表中

                else:
                    # print(f'第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')
                    # json_data = json.dumps({'url': table_url}, indent=4)
                    # df_json_list.append(json_data)
                    continue
            except Exception as e:
                # 打印异常信息
                # print(f'第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')
                # json_data = json.dumps({'url': table_url}, indent=4)
                # df_json_list.append(json_data)
                # print(f'{e}，但是url已保存，第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')

                print(f'错误信息{e}')
        # 将JSON字符串列表转换回字典列表
        json_list = [json.loads(item) for item in df_json_list]
        # 将字典列表转换为DataFrame格式
        dfj = pd.DataFrame(json_list)
        # 打印最终的DataFrame数据
        print(dfj)
        return dfj

    def crawl_table(self, url_list):
        # 遍历每个网址以获取并处理表格数据
        concat_df = pd.DataFrame()
        for i, table_url in enumerate(url_list):
            try:
                # 从网址中读取HTML表格数据
                tables = pd.read_html(table_url)
                for table in tables:
                    print(f'第{i + 1}个网址已经处理完成，还剩{len(url_list) - i - 1}个网址需要处理')
                    concat_df = pd.concat([concat_df, table], ignore_index=True)
            except Exception as e:
                # 打印异常信息
                print(e)
        return concat_df


if __name__ == '__main__':
    # excel_data = crawl_table(url)
    file_name = input('输入文件名称: ')
    # print(excel_data)
    key_words = input('输入关键词: ')
    df = pd.read_excel(f'../data_source/{file_name}')
    # excel_data.to_excel('../data/japan_bus_info.xlsx', index=False)
    cral = CrawlData(dataf=df, key_word=key_words)
    cral.crawl_data().to_excel('../data/text.xlsx', index=False)
