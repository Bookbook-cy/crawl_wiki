import cx_Oracle
import os

# 数据库连接配置
connection = cx_Oracle.connect("OJADMIN/123456@127.0.0.1:1522/oracle")
cursor = connection.cursor()

# 输出目录
output_dir = "D:/output_images/Exported"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 查询BLOB数据并导出
def export_blobs_to_images():
    try:
        cursor = connection.cursor()

        # 查询BLOB数据和文件名
        query = """
        SELECT OJ_PIC,OJ_IDNO || '.jpg' AS file_name FROM BAK_OJDT_PERSON_PIC_E1
        """
        cursor.execute(query)

        # 遍历结果并导出图片
        for lob_data, file_name in cursor:
            #file_path = os.path.join(output_dir, file_name)
            base_name, ext = os.path.splitext(file_name)
            output_path = os.path.join(output_dir, f"{base_name}{ext}")
            
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(output_dir, f"{base_name}_{counter}{ext}")
                counter += 1
               
            with open(output_path, 'wb') as file:
                file.write(lob_data.read())
            print(f"Exported: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# 执行导出
export_blobs_to_images()