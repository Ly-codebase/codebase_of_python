"""
模块名称: text_translation
功能描述: 本脚本用于读取Excel文件中的数据，判断某一列是中文、英文还是拼音，并进行相应的操作。
创建日期: 2023-11-27
最后修改日期: 2024-11-27
版本: 1.0
依赖库: pandas, pypinyin, googletrans, re
"""

import pandas as pd
from pypinyin import lazy_pinyin
from googletrans import Translator
import re

def is_chinese(text):
    """
    判断文本是否为中文。

    参数:
        text (str): 待判断的文本。

    返回:
        bool: 如果文本是中文，则返回True；否则返回False。
    """
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def is_english(text):
    """
    判断文本是否为英文。

    参数:
        text (str): 待判断的文本。

    返回:
        bool: 如果文本是英文，则返回True；否则返回False。
    """
    return bool(re.match(r'^[a-zA-Z\s]+$', text))

def is_pinyin(text):
    """
    判断文本是否为拼音。

    参数:
        text (str): 待判断的文本。

    返回:
        bool: 如果文本是拼音，则返回True；否则返回False。
    """
    # 拼音通常由字母和空格组成
    return bool(re.match(r'^[a-z\s]+$', text.lower()))

def chinese_to_pinyin(text):
    """
    将中文文本转换为拼音。

    参数:
        text (str): 中文文本。

    返回:
        str: 对应的拼音字符串。
    """
    return ' '.join(lazy_pinyin(text))

def translate_text(text, src_lang, dest_lang):
    """
    翻译文本。

    参数:
        text (str): 待翻译的文本。
        src_lang (str): 源语言代码，例如'zh-cn'或'en'。
        dest_lang (str): 目标语言代码，例如'zh-cn'或'en'。

    返回:
        str: 翻译后的文本。
    """
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def translate_excel(file_path, column_name):
    """
    处理Excel文件，判断指定列的内容是中文、英文还是拼音，并进行相应的操作。

    参数:
        file_path (str): Excel文件路径。
        column_name (str): 需要处理的列名。
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 获取需要处理的列
    column_data = df[column_name]

    # 创建新的列来存储处理后的结果
    df['Processed'] = ''

    for index, value in column_data.items():
        if is_chinese(value):# 将中文转化为拼音和英文
            df.at[index, 'Processed_English'] = translate_text(value, 'zh-ch', 'en')
            df.at[index, 'Processed_Pinyin'] = chinese_to_pinyin(value)
        elif is_english(value): # 将英文转化为中文
            df.at[index, 'Processed'] = translate_text(value, 'en', 'zh-cn')

        else:
            df.at[index, 'Processed'] = 'Unknown'
    # 打印处理后的结果
    print(df)
    '''
    # 保存结果到新的Excel文件
    output_file_path = 'processed_' + os.path.basename(file_path)
    df.to_excel(output_file_path, index=False)
    print(f"Data has been written to {output_file_path}")
    '''

if __name__ == '__main__':
    # 读取Excel文件
    file_path = "C:/Users/luyi/Desktop/新建 Microsoft Excel 工作表.xlsx"
    column_name = 'text'

    # 处理Excel文件
    translate_excel(file_path, column_name)