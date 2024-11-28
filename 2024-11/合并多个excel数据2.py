import pandas as pd  
import os  
  
# 定义Excel文件的文件夹路径  
folder_path = 'D:/edge下载/parts_of_data_ly - 副本'
  
# 获取文件夹中的所有Excel文件  
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.csv') ]#or f.endswith('.xls')]  
  
# 初始化一个空的DataFrame来存储合并后的数据  
combined_df = pd.DataFrame()  
  
# 遍历所有Excel文件并合并它们  
for file in excel_files:  
    file_path = os.path.join(folder_path, file)  
    # 读取Excel文件，假设所有的Excel文件都有一个名为'  '的工作表  
    df = pd.read_csv(file_path )#sheet_name='Sheet1')  
    # 提取文件名（不包含路径和扩展名）  
    file_name = os.path.splitext(os.path.basename(file))[0]  
      
    # 添加一个新列来存储文件名  
    df['文件名'] = file_name  
      
    # 将读取到的DataFrame追加到combined_df中  
    combined_df = pd.concat([combined_df, df], ignore_index=True)  
  
# 将合并后的数据写入一个新的Excel文件  
combined_df.to_csv('C:/Users/luyi/Desktop/result_file_of_all.csv', index=False)  
  
print("Excel files have been successfully merged into one with filenames as a new column.")