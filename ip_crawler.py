from playwright.sync_api import sync_playwright
import time
import random
from fake_useragent import UserAgent

def get_stealth_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.kuaidaili.com/'
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
        
        with open('proxies.txt', 'w', encoding='utf-8') as f:
            for page_num in range(1, 101):
                try:
                    url = f'https://www.kuaidaili.com/free/inha/{page_num}/'
                    
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