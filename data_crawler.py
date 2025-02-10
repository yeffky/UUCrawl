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
    try:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
            if proxies:
                return random.choice(proxies)
    except FileNotFoundError:
        pass
    return None

def remove_invalid_proxy(proxy):
    try:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
        
        if proxy in proxies:
            proxies.remove(proxy)
        
        with open('proxies.txt', 'w') as f:
            f.write('\n'.join(proxies) + '\n')
    except FileNotFoundError:
        pass

def make_request(url, payload, auth, timestamp):
    ua = UserAgent()
    headers = {'User-Agent': 'Apifox/1.0.0 (https://apifox.com)', 'Auth': str(auth), 'Timestamp': str(timestamp), "Content-Type":"application/json",}
    proxy = get_random_proxy()
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
    base_url = "https://api-csob.ok-skins.com/api/v1/rank"
    payload = {
        "category": [],
        "minPrice": 100000,
        "minSellCount": 30,
        "sellCountType": "DOWN",
        "sellCountTimeRange": "WEEK",
        "sellCountChange": 15,
        "categoryInclude": "TRUE",
        "exterior": [],
        "quality": [],
        "rarity": [],
        "exteriorInclude": "TRUE",
        "qualityInclude": "TRUE",
        "rarityInclude": "TRUE",
        "priceChangePercentTimeRange": "HALF_MONTH",
        "container": [],
        "containerInclude": "TRUE",
        "nameInclude": "TRUE",
        "leaseCountType": "DOWN",
        "leaseCountTimeRange": "WEEK",
        "leaseCountChange": 100,
        "volCountTimeRange": "WEEK",
        "volLeaseCountTimeRange": "WEEK",
        "maxPrice": 500000,
        "minLeaseCount": 20,
        "maxLeaseCount": 50,
        "type": "LEASE",
        "page": 1
    }
    
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
        filename = f'goods_{today_date}.txt'

        with open(filename, 'w', encoding='utf-8') as f:
            for item in items_list:
                item_str = json.dumps(item, ensure_ascii=False, indent=2)
                f.write(item_str + '\n\n')
        
        print(f"Successfully wrote {len(items_list)} items to goods.txt")
    except json.JSONDecodeError:
        print("Failed to decode JSON response")

if __name__ == "__main__":
    crawl_data()
