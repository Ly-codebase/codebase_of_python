import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main(file_path):
    """
    绘制小提琴图。

    参数: 
    file_path:excel的文件路径

    返回：
    None
    """
    # 读取Excel文件中的数据
    df = pd.read_excel(file_path)

    # 检查award_age_category的唯一值数量
    unique_categories = df['award_age_category'].nunique()
    print(f"Unique categories in award_age_category: {unique_categories}")

    # 设置Seaborn的样式
    sns.set(style="whitegrid")

    # 设置支持中文的字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    # 获取需要绘制的指标列表（除去分类依据'award_age_category'）
    metrics = ['H_index', 'T_value', 'P_value']

    # 定义调色板
    #A2C4F1 #CEBAF0 #C6C3E1
    custom_palette = ["#A2C4F1", "#CEBAF0", "#C6C3E1"]  # 更美观的颜色

    # 创建图形窗口（根据metrics数量调整）
    n_plots = len(metrics)
    rows = (n_plots // 2) + (n_plots % 2)  # 计算行数
    cols = 3 if n_plots > 1 else 1  # 列数最多为3
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(12, 12))  # 减小图形窗口的大小
    if n_plots == 1:
        axes = [axes]  # 如果只有一个图，将axes转换为列表
    else:
        axes = axes.flatten()  # 将axes展平为一维数组

    # 如果有空闲的子图，先创建占位符，稍后在循环中填充
    for ax in axes:
        ax.set_visible(False)  # 初始设置为不可见，后续根据metrics数量决定是否显示

    # 绘制每个指标的小提琴图
    for i, metric in enumerate(metrics):
        axes[i].set_visible(True)  # 使当前子图可见
        sns.violinplot(x='award_age_category', y=metric, data=df, palette=custom_palette, inner="quartile", ax=axes[i])
        axes[i].set_title(f'{metric}')
        axes[i].set_xlabel('award_age_category')
        axes[i].set_ylabel(metric)


    # 调整子图之间的间距
    plt.subplots_adjust(hspace=0.8, wspace=0.5)

    # 显示图形
    plt.show()

# 当脚本被直接运行时，调用main()函数
if __name__ == '__main__':
    file_path = "C:/Users/luyi/Desktop/数据/数据可视化/小提琴图/小提琴图.xlsx"
    main(file_path)