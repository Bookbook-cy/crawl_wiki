import pandas as pd

# 维基百科页面 URL
url = 'https://en.wikipedia.org/wiki/Adilabad%E2%80%93Hazur_Sahib_Nanded_Express'
# 使用 pandas 读取网页中的所有表格
tables = pd.read_html(url)
total_df = pd.DataFrame()

# 输出表格数量
print(f"共找到 {len(tables)} 个表格。")

# 遍历并显示每个表格的前几行
for i, table in enumerate(tables):
    print(f"\n表格 {i + 1}:")
    print(table)
    # total_df = pd.concat([total_df, table], ignore_index=True)
# tables[4].to_excel('./data/ind_railway.xlsx')
