import os
import pandas as pd
from sqlalchemy import engine

# 设置文件夹路径
folder_path = 'D:/项目文件/交通出行/台湾/驾驶和交通安全'

# engineing = engine.create_engine('mysql+pymysql://root:123456@localhost:3306/dxsz')
# 创建一个空的 DataFrame 来存储所有合并的数据
# combined_df = pd.DataFrame()

# # 遍历文件夹中的所有文件
# for file_name in os.listdir(folder_path):
#     # 检查文件是否为 Excel 文件
#     if file_name.endswith('.xlsx'):
#         # 构建文件的完整路径
#         file_path = os.path.join(folder_path, file_name)
#
#         # 读取 Excel 文件并合并到 combined_df 中
#         df = pd.read_excel(file_path, sheet_name='Sheet1')
#         combined_df = pd.concat([combined_df, df], ignore_index=True)
#
#         print(f"已加载文件：{file_name}")
#
# # 将合并后的 DataFrame 保存为新的 Excel 文件
# combined_df.to_excel('D:/项目文件/zc/数据采集/日本/USAcombined.xlsx', index=False)
#
# print( "数据合并完成！")


combin_df = pd.DataFrame()
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)

        df = pd.read_excel(file_path, sheet_name='Sheet1')
        combin_df = pd.concat([combin_df, df], ignore_index=True)

        print(f"已加载文件：{file_name}")
combin_df.to_excel('D:/项目文件/交通出行/台湾/驾驶和交通安全/驾驶和交通安全.xlsx')