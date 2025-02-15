'''
Author: yeffky
Date: 2025-02-14 09:41:09
LastEditTime: 2025-02-15 10:44:51
'''
from playwright.sync_api import sync_playwright
import time
import re

def generate_pic(url):
    # 启动浏览器
    player = sync_playwright().start()  # 初始化Playwright并启动
    chrome_driver = player.chromium  # 获取Chromium浏览器实例
    browser = chrome_driver.launch(headless=False)  # 启动浏览器，headless=False表示以非无头模式启动，即显示浏览器窗口
    context = browser.new_context()  # 创建一个新的浏览器上下文（类似于一个新的浏览器窗口）
    page = context.new_page()  # 在该上下文中创建一个新的页面（标签页）
    # 访问页面
    card_cnt = 0
    with(open('./pic_generate/pic.html', 'r', encoding='utf-8')) as f:
        page_content = f.read()
        card_cnt = len(re.findall(r'<div class="card" id="card\d+">', page_content))
    print(card_cnt)
    page.goto(url)  # 导航到指定的URL
    #  截取相关卡片的截图
    for i in range(1, card_cnt + 1):
        card_pic = page.query_selector(f"id=card{i}")  # 使用CSS选择器查找页面中的搜索按钮元素
        card_pic.screenshot(path=f"./pictures/card{i}.png")  # 对搜索按钮元素进行截图并保存为b.png

    # 停止访问
    context.close()  # 关闭浏览器上下文
    browser.close()  # 关闭浏览器
    player.stop()  # 停止Playwright
    
if __name__ == '__main__':
    url = 'D:/Project/UUCrawl/Code/pic_generate/pic.html'
    generate_pic(url)