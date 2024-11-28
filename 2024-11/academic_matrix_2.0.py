"""
模块名称: academic_matrix-2.0
功能描述: 本脚本用于批量处理指定文件夹内的CSV格式的学者数据文件，计算每个学者的学术迹（Academic Trace）及其他相关指标，
并将结果合并保存到一个新的Excel文件中。
作者: luyi
创建日期: 2023-11-27
最后修改日期: 2024-11-27
版本: 1.0
依赖库: pandas, csv, os
"""

import pandas as pd
import csv
import os

def read_csv_cell(file_path, row_index, col_index):
    """
    从指定的CSV文件中读取特定行和列的数据。

    参数:
        file_path (str): CSV文件路径。
        row_index (int): 要读取的行索引。
        col_index (int): 要读取的列索引。

    返回:
        str or None: 如果找到，则返回单元格内容；否则返回None。
    """
    with open(file_path, mode='r', newline='', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row_idx, row in enumerate(csv_reader):
            if row_idx == row_index:
                if 0 <= col_index < len(row):
                    return row[col_index]
                else:
                    return None  # 列索引超出范围
        return None  # 行索引超出范围


def get_academic_matrix(file_path, h_index):
    """
    计算学术迹（T）。

    参数:
        file_path (str): CSV文件路径。
        h_index (int): 学者的H指数。

    返回:
        float: 学术迹（T）。
    """
    df = pd.read_csv(file_path, header=12, names=['文献顺序', '引文', '标题'])
    df_from_15th_row = df.iloc[14:]
    P = df_from_15th_row['引文'].count()
    C = df_from_15th_row['引文'].sum()
    P_z = df_from_15th_row[df_from_15th_row['引文'] == 0]['引文'].count()
    P_c = df_from_15th_row[df_from_15th_row['引文'] <= h_index]['引文'].count()
    C_t = h_index ** 2
    C_e = df_from_15th_row[df_from_15th_row['引文'] >= h_index]['引文'].sum() - C_t
    T = P_c**2 / P + C_t**2 / C + C_e**2 / C - P_z**2 / P
    return T


def get_p_value(file_path):
    """
    计算P值。

    参数:
        file_path (str): CSV文件路径。

    返回:
        float: P值。
    """
    df = pd.read_csv(file_path, header=12, names=['文献顺序', '引文', '标题'])
    df_from_15th_row = df.iloc[14:]
    P = df_from_15th_row['引文'].count()
    C = df_from_15th_row['引文'].sum()
    P_value = (C**2 / P) ** (1/3)
    return P_value


def process_files(folder_path):
    """
    处理指定文件夹内的所有CSV文件，计算每个文件的学术迹和其他指标，并将结果合并保存到一个Excel文件中。

    参数:
        folder_path (str): 包含CSV文件的文件夹路径。
    """
    # 获取文件夹中的所有CSV文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    # 初始化一个空的DataFrame来存储合并计算后的数据
    combined_df = pd.DataFrame()

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        try:
            # 读取h指数
            h_index = int(read_csv_cell(file_path, 5, 1))
            # 读取作者信息
            author_name = read_csv_cell(file_path, 2, 1)
            scopus_id = read_csv_cell(file_path, 3, 1)
            start_year = read_csv_cell(file_path, 7, 1)
            end_year = read_csv_cell(file_path, 8, 1)

            # 计算学术迹T
            T = get_academic_matrix(file_path, h_index)
            # 计算P值
            P_value = get_p_value(file_path)

            data = {
                'Scopus ID': [scopus_id],
                'Author Name': [author_name],
                'Start Year': [start_year],
                'End Year': [end_year],
                'H-Index': [h_index],
                'Academic Trace (T)': [T],
                'P_value': [P_value]
            }

            df = pd.DataFrame(data)
            # 将读取到的DataFrame追加到combined_df中
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # 指定新的Excel文件的路径
    excel_file_path = 'result_file-3.xlsx'
    # 使用pandas的to_excel方法将数据写入Excel文件
    combined_df.to_excel(excel_file_path, index=False)
    print(f"Data has been written to {excel_file_path}")


if __name__ == '__main__':
    # 修改csv文件的文件夹路径
    folder_path = "D:/edge下载/parts_of_data_sjr"
    process_files(folder_path)