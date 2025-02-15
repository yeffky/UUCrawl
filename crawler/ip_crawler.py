'''
Author: yeffky
Date: 2025-02-09 18:34:01
LastEditTime: 2025-02-15 10:53:18
'''
from playwright.sync_api import sync_playwright
import time
import random
from fake_useragent import UserAgent
import json

def get_stealth_headers():
    # 创建一个UserAgent对象，用于生成随机的用户代理字符串
    ua = UserAgent()
    referer = json.loads(open('docs/ip_crawl_config.json', 'r', encoding='utf-8').read())['referer']
    
    # 返回一个字典，包含用于伪装请求的HTTP头部信息
    return {
        # 设置User-Agent头部，使用UserAgent对象生成的随机用户代理字符串
        'User-Agent': ua.random,
        # 设置Accept-Language头部，表示客户端接受的语言，这里设置为英语
        'Accept-Language': 'en-US,en;q=0.9',
        # 设置Referer头部，表示请求的来源页面
        'Referer': referer
    }

def scrape_with_playwright():
    with sync_playwright() as p:
        # 启动带反检测设置的浏览器
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )
        
        context = browser.new_context(
            user_agent=get_stealth_headers()['User-Agent'],
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers=get_stealth_headers()
        )
        
        # 禁用WebDriver属性
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        page = context.new_page()
        
        base_url = json.loads(open('docs/ip_crawl_config.json', 'r', encoding='utf-8').read())['base_url']
        with open('proxies.txt', 'w', encoding='utf-8') as f:
            for page_num in range(1, 101):
                try:
                    url = f'{base_url}/{page_num}/'
                    # 添加随机页面行为
                    page.mouse.move(
                        random.randint(0, 1920),
                        random.randint(0, 1080)
                    )
                    
                    page.goto(url, timeout=60000)
                    
                    # 随机滚动页面
                    for _ in range(random.randint(1, 3)):
                        page.mouse.wheel(0, random.randint(300, 800))
                        time.sleep(0.5)
                    
                    # 等待表格加载（根据实际需要调整选择器）
                    page.wait_for_selector('table tbody tr', timeout=15000)
                    
                    # 解析表格数据
                    rows = page.query_selector_all('table tbody tr')
                    for row in rows:
                        ip = row.query_selector('td:first-child').inner_text().strip()
                        port = row.query_selector('td:nth-child(2)').inner_text().strip()
                        f.write(ip + ':' + port + '\n')
                    
                    print(f'第 {page_num} 页完成，获取 {len(rows)} 条代理')
                    
                    # 随机延时（3-8秒更自然）
                    time.sleep(random.uniform(3, 8))
                    
                    # 定期清除cookies
                    if page_num % 10 == 0:
                        context.clear_cookies()
                        
                except Exception as e:
                    print(f'第 {page_num} 页异常：{str(e)}')
                    continue

        browser.close()

if __name__ == '__main__':
    scrape_with_playwright()
    print('数据已保存至proxies.txt')