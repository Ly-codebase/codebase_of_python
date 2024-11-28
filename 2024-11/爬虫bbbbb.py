from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def search_wos(title):
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
        
        print(f'Title: {title}')
        print(f'Year: {year}')
    
    finally:
        # 关闭浏览器
        print("Closing the browser...")
        driver.quit()


if __name__ == "__main__":
    article_title = "PVNET: Pixel-wise voting network for 6dof pose estimation"
    search_wos(article_title)