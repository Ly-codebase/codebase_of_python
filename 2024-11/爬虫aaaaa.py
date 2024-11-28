from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        try:
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="search-option"]')))
        except Exception as e:
            print(f"Error finding the search box element: {e}")
            search_box = None
        
        if search_box is None:
            print("Search box not found. Exiting.")
            return
        
        # 输入文章标题
        search_box.send_keys(title)
        search_box.send_keys(Keys.RETURN)
        
        # 等待搜索结果加载
        try:
            results_page = wait.until(EC.presence_of_element_located((By.XPATH, '//app-records-list')))
        except Exception as e:
            print(f"Error finding the results page element: {e}")
            results_page = None
        
        if results_page is None:
            print("Results page not found. Exiting.")
            return
        
        # 使用提供的XPath表达式获取发表年份
        year_xpath = '//span[@name="pubdate" and @data-ta="summary-record-pubdate"]'
        
        try:
            year_element = wait.until(EC.presence_of_element_located((By.XPATH, year_xpath)))
            year = year_element.text
        except Exception as e:
            print(f"Error finding the year element: {e}")
            year = "Not found"
        
        print(f'Title: {title}')
        print(f'Year: {year}')
    
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    article_title = "PVNET: Pixel-wise voting network for 6dof pose estimation"
    search_wos(article_title)