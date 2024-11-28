'''
------------
2024-11
该代码的作用为批量读取CSV（或excel）文件，
将每个文件中的前几行（提取有用值，并去除）进行处理
最后得到新的文件
输入：文件夹地址
输出：处理后文件
------------
'''
import os
import pandas as pd
from glob import glob

def process_csv(file_path):
    try:
        # 读取CSV文件的前14行
        header_df = pd.read_csv(file_path, header=None, nrows=14, error_bad_lines=False, warn_bad_lines=True)
        
        # 获取第四行（索引3）第二列（索引1）的作者ID
        if len(header_df) > 3:  # 确保文件至少有四行
            author_id = header_df.iloc[3, 1]
        else:
            author_id = None  # 如果文件没有足够的行，则设置author_id为None
        
        # 读取剩余的CSV文件内容，跳过前14行
        df = pd.read_csv(file_path, header=None, skiprows=14, error_bad_lines=False, warn_bad_lines=True)
        
        # 检查列数是否一致
        expected_columns = 3  # 假设剩余部分应该有3列
        if df.shape[1] != expected_columns:
            raise ValueError(f"Column count mismatch: Expected {expected_columns} columns, but found {df.shape[1]} columns.")
        
        # 添加新的列'作者ID'
        df['作者ID'] = author_id
        
        # 去除最后一行
        if not df.empty:
            df = df[:-1]
        
        # 重置列名
        df.columns = ['文献顺序', '引文', '标题', '作者ID']
        
        # 写回原文件
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Processed {file_path} successfully.")
    
    except pd.errors.EmptyDataError:
        print(f"Warning: {file_path} is empty.")
    except pd.errors.ParserError as pe:
        print(f"Warning: {file_path} has parsing errors. Details: {pe}")
    except ValueError as ve:
        print(f"Warning: {file_path} has column count mismatch. Details: {ve}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def batch_process_csvs(directory):
    # 获取目录下所有的CSV文件
    csv_files = glob(os.path.join(directory, '*.csv'))
    
    # 对每个文件执行处理
    for file in csv_files:
        process_csv(file)

# 指定需要处理的文件夹路径
directory_path = 'D:/edge下载/parts_of_data_ly - 副本'

# 执行批量处理
batch_process_csvs(directory_path)