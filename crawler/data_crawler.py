'''
Author: yeffky
Date: 2025-02-09 17:18:05
LastEditTime: 2025-03-03 15:34:44
'''
import requests
import random
import time
import json
from fake_useragent import UserAgent
import hashlib
import time
from datetime import datetime


# 定义md5加密函数
def md5_hash(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

# Le函数，类似于JS中的Le函数
def getAuth(e):
    # 第一次MD5，将输入转换为字符串并计算MD5
    first_md5 = hashlib.md5(str(e).encode()).hexdigest()
    # 拼接字符串并第二次计算MD5
    combined = first_md5 + "pc*&bQ2@mkvt"
    second_md5 = hashlib.md5(combined.encode()).hexdigest()
    return second_md5

def get_random_proxy():
    # 尝试打开名为 'proxies.txt' 的文件
    try:
        with open('proxies.txt', 'r') as f:
            # 读取文件内容并按行分割成列表
            proxies = f.read().splitlines()
            # 如果列表不为空，则随机选择一个代理并返回
            if proxies:
                return random.choice(proxies)
    # 如果文件不存在，则捕获 FileNotFoundError 异常并忽略
    except FileNotFoundError:
        pass
    # 如果文件不存在或列表为空，则返回 None
    return None

def remove_invalid_proxy(proxy):
    # 尝试执行以下代码块，如果发生异常则跳转到except块
    try:
        # 打开名为'proxies.txt'的文件，以读取模式('r')
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
        
        if proxy in proxies:
        # 检查传入的proxy是否在proxies列表中
            proxies.remove(proxy)
        
        with open('proxies.txt', 'w') as f:
            f.write('\n'.join(proxies) + '\n')
    except FileNotFoundError:
        pass

def make_request(url, payload, auth, timestamp):
    # 创建一个UserAgent对象，用于生成随机的User-Agent字符串
    ua = UserAgent()
    headers = {'User-Agent': ua.random, 'Auth': str(auth), 'Timestamp': str(timestamp), "Content-Type":"application/json",}
    proxy = get_random_proxy() # 获取一个随机的代理
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    
    try:
        response = requests.post(
            url,
            headers=headers,
            timeout=10, 
            # proxies=proxies,
            json=payload, 
            # verify=False
        )
        response.raise_for_status()
        print(response)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        
        # If the request failed, remove the invalid proxy
        # if proxy:
        #     remove_invalid_proxy(proxy)
        
        # Try a new proxy
        return None

def crawl_data():
    # 加载爬虫配置文件
    crawal_config = json.load(open('./docs/crawl_config.json', 'r'))
    base_url = crawal_config['base_url']  # 获取基础URL
    payload = crawal_config['payload']  # 获取请求负载
    
    response_text = None
    while not response_text:  # Retry until the request is successful
        # 时间戳
        t = int((time.time()) * 1000)  # 获取当前时间戳（毫秒）
        auth = getAuth(t)
        response_text = make_request(base_url, payload, auth, t)
        if not response_text:
            print("Retrying with a new proxy...")
            time.sleep(random.randint(3, 5))  # Add a small delay before retrying

    try:
        data = response_text
        items_list = data.get('data', {}).get('list', [])
        
        # 获取今天的日期
        today_date = datetime.now().strftime('%Y-%m-%d')

        # 在文件名后加上今天的日期
        filename = f'goods_{today_date}.json'
        cnt = 0
        with open(f'data/{filename}', 'w', encoding='utf-8') as f:
            f.write('{"items": [' + '\n')
            for item in items_list:
                item['饰品涨幅'] = item.pop('minPriceChangePercent')
                item['出租热度'] = item.pop('leaseCountChange7')
                item['商品名称'] = item.pop('goodsName')
                item['price'] = item['price'] / 100
                item['商品最低价'] = item.pop('price')
                item['leasePrice'] = item['leasePrice'] / 100
                item['短租最低价'] = item.pop('leasePrice')
                item['longLeasePrice'] = item['longLeasePrice'] / 100
                item['长租最低价'] = item.pop('longLeasePrice')
                item['商品图标'] = item.pop('iconUrl')
                item['value'] = 19200 * item['value']
                item['短租年化'] = item.pop('value')
                cnt += 1
                item_str = json.dumps(item, ensure_ascii=False, indent=2)
                if cnt == len(items_list):
                    f.write(item_str + '\n')
                else:
                    f.write(item_str + ',\n\n')
            f.write(']}' + '\n')
        print(f"Successfully wrote {len(items_list)} items to goods.txt")
    except json.JSONDecodeError:
        print("Failed to decode JSON response")

if __name__ == "__main__":
    crawl_data()
