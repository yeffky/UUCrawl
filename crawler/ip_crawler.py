from playwright.sync_api import sync_playwright
import time
import random
from fake_useragent import UserAgent
import json
from concurrent.futures import ThreadPoolExecutor

def fetch_ip(url):
    """每个线程使用独立的浏览器实例"""
    with sync_playwright() as p:
        try:
            # 初始化浏览器实例
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-setuid-sandbox'
                ]
            )
            
            # 创建新的上下文
            context = browser.new_context(
                user_agent=get_stealth_headers()['User-Agent'],
                viewport={'width': 1920, 'height': 1080},
                extra_http_headers=get_stealth_headers()
            )
            
            # 反检测脚本
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)

            page = context.new_page()
            
            # 随机鼠标移动
            page.mouse.move(
                random.randint(0, 1920),
                random.randint(0, 1080)
            )
            
            # 访问页面
            page.goto(url, timeout=60000)
            
            # 随机滚动
            for _ in range(random.randint(1, 3)):
                page.mouse.wheel(0, random.randint(300, 800))
                time.sleep(0.5)
            
            # 等待表格加载
            page.wait_for_selector('table tbody tr', timeout=15000)
            
            # 解析数据
            rows = page.query_selector_all('table tbody tr')
            ip_list = []
            for row in rows:
                try:
                    ip = row.query_selector('td:first-child').inner_text().strip()
                    port = row.query_selector('td:nth-child(2)').inner_text().strip()
                    ip_list.append(f'{ip}:{port}')
                except:
                    continue
                    
            return ip_list
            
        except Exception as e:
            print(f'请求 {url} 失败: {str(e)}')
            return []
        finally:
            # 确保资源释放
            if 'page' in locals():
                page.close()
            if 'context' in locals():
                context.close()
            if 'browser' in locals():
                browser.close()

def get_stealth_headers():
    ua = UserAgent()
    config = json.load(open('docs/ip_crawl_config.json', 'r', encoding='utf-8'))
    return {
        'User-Agent': ua.random,
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': config['referer']
    }

def crawl_ip():
    config = json.load(open('docs/ip_crawl_config.json', 'r', encoding='utf-8'))
    base_url = config['base_url']
    urls = [f'{base_url}/{page_num}/' for page_num in range(1, 20)]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(fetch_ip, urls)
        
        with open('./docs/proxies.txt', 'w', encoding='utf-8') as f:
            total = 0
            for idx, ip_list in enumerate(results, 1):
                if ip_list:
                    f.write('\n'.join(ip_list) + '\n')
                    print(f'第 {idx} 页获取到 {len(ip_list)} 条代理')
                    total += len(ip_list)
            print(f'共获取 {total} 条代理')
