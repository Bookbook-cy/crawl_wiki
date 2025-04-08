import pandas as pd

url = 'https://zh.wikipedia.org/wiki/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E7%AF%80%E6%97%A5%E8%88%87%E6%AD%B2%E6%99%82%E5%88%97%E8%A1%A8'

railways_list = pd.read_html(url)
table_list = []
table_df = pd.DataFrame()
for i, table in enumerate(railways_list):
    print(f"表格 {i + 1}:")
    print(table)
    table_list.append(table)

# print(table_list)
result = pd.concat([table_df] + [table_list[i] for i in [0, 1, 2]], ignore_index=True)
# result = pd.concat([table_df] + [table_list[0]], ignore_index=True)
#
print(result)
result.to_excel("../msmf_data/tw_festivals_data.xlsx", index=False)
print('completed')
