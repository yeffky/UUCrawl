'''
Author: yeffky
Date: 2025-02-14 09:41:09
LastEditTime: 2025-02-20 09:58:15
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import shutil
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 构造本地文件的URL路径
file_path = 'D:/Project/UUCrawl/Code/pic_generate/pic.html'
target_url = f'file:///{file_path}'
    

def generate_pic(url):
    import os


    # 清空目录但保留空文件夹
    folder = './pictures'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # 删除文件
        except Exception as e:
            print(f'删除 {file_path} 失败: {e}')
    # 确保截图保存目录存在
    os.makedirs('./pictures', exist_ok=True)
    service = Service(executable_path=ChromeDriverManager().install())
    # 使用Selenium启动Chrome浏览器
    driver = webdriver.Chrome(service=service)  # 确保ChromeDriver在PATH环境变量中
    
    try:
        # 访问目标页面
        driver.get(url)
        # 最大化浏览器窗口以确保元素可见
        driver.maximize_window()
        # 等待页面加载完成（可根据实际情况调整）
        time.sleep(2)
        
        # 查找所有卡片元素
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.card[id^="card"]')
        print(f"Found {len(cards)} cards")
        
        # 遍历每个卡片进行截图
        for card in cards:
            # 获取卡片ID
            card_id = card.get_attribute('id')
            card_number = card_id.replace('card', '')
            
            # 滚动到元素位置
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
            # 等待滚动完成
            time.sleep(0.5)
            
            # 截图并保存
            card.screenshot(f'./pictures/card{card_number}.png')
            print(f"Screenshot saved for {card_id}")
            
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == '__main__':
    generate_pic(target_url)