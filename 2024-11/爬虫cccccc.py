from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def get_titles_from_csv(file_path, column_name='title'):
    """
    从指定的CSV文件中读取指定列的标题。
    
    :param file_path: CSV文件的路径
    :param column_name: 包含标题的列名，默认为'Title'
    :return: 标题列表
    """
    df = pd.read_csv(file_path,encoding='gb18030')
    titles = df[column_name].tolist()
    return titles

def search_wos(title, file_path):
    """
    在Web of Science上根据文章标题搜索并获取其发表年份，然后将年份信息写入CSV文件。
    
    :param title: 文章标题
    :param file_path: CSV文件的路径
    """
    # 设置ChromeDriver的路径
    driver_path = 'C:/Program Files/Google/Chrome/Application/chromedriver.exe'
    
    # 创建Service对象
    service = Service(executable_path=driver_path)
    
    # 初始化WebDriver
    driver = webdriver.Chrome(service=service)
    
    try:
        # 打开Web of Science网站
        driver.get("https://webofscience.clarivate.cn/wos/woscc/basic-search")
        
        # 等待页面加载
        wait = WebDriverWait(driver, 30)  # 增加等待时间
        print("Waiting for the search field dropdown to be present...")
        
        # 选择检索字段的下拉菜单
        search_field_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//wos-select[@data-ta="search-field-dropdown"]//button')))
        print("Search field dropdown found.")
        
        # 使用JavaScript点击下拉菜单
        driver.execute_script("arguments[0].click();", search_field_dropdown)
        
        # 等待选项加载
        time.sleep(1)  # 等待选项加载
        
        # 选择“标题”选项
        title_option_xpath = '//div[@role="menuitem" and @title="Title"]'
        title_option = wait.until(EC.element_to_be_clickable((By.XPATH, title_option_xpath)))
        print("Title option found.")
        
        # 使用JavaScript点击“标题”选项
        driver.execute_script("arguments[0].click();", title_option)
        
        # 等待搜索框出现
        try:
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="search-option"]')))
            print("Search box found.")
        except Exception as e:
            print(f"Error finding the search box element: {e}")
            search_box = None
        
        if search_box is None:
            print("Search box not found. Exiting.")
            return
        
        # 输入文章标题
        print("Entering the article title...")
        search_box.send_keys(title)
        search_box.send_keys(Keys.RETURN)
        
        # 等待搜索结果加载
        print("Waiting for the results page to load...")
        try:
            results_page = wait.until(EC.presence_of_element_located((By.XPATH, '//app-records-list')))
            print("Results page loaded.")
        except Exception as e:
            print(f"Error finding the results page element: {e}")
            results_page = None
        
        if results_page is None:
            print("Results page not found. Exiting.")
            return
        
        # 使用提供的XPath表达式获取发表年份
        year_xpath = '//span[@name="pubdate" and @data-ta="summary-record-pubdate"]'
        
        print("Waiting for the year element to be present...")
        try:
            year_element = wait.until(EC.presence_of_element_located((By.XPATH, year_xpath)))
            year = year_element.text
            print("Year element found.")
        except Exception as e:
            print(f"Error finding the year element: {e}")
            year = "Not found"
        
        # 更新CSV文件
        update_csv_with_year(file_path, title, year)
    
    finally:
        # 关闭浏览器
        print("Closing the browser...")
        driver.quit()

def update_csv_with_year(file_path, title, year):
    """
    将获取到的文章发表年份更新到CSV文件中。
    
    :param file_path: CSV文件的路径
    :param title: 文章标题
    :param year: 文章发表年份
    """
    df = pd.read_csv(file_path,encoding='gb18030')
    # 假设CSV文件中有一列名为'Year'用于存储年份，如果不存在则创建
    if 'Year' not in df.columns:
        df['Year'] = ''
    
    # 更新特定标题对应的年份
    df.loc[df['title'] == title, 'Year'] = year
    
    # 保存更新后的数据到CSV文件
    df.to_csv(file_path, index=False,encoding='gb18030')

if __name__ == "__main__":
    csv_file_path =  'C:/Users/luyi/Desktop/result_file_of_all-4.csv'  # 指定CSV文件路径
    titles = get_titles_from_csv(csv_file_path)
    
    for title in titles:
        print(f'Searching for: {title}')
        search_wos(title, csv_file_path)
     
