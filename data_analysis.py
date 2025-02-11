'''
Author: yeffky
Date: 2025-02-11 11:17:04
LastEditTime: 2025-02-11 20:26:21
'''
import json
import os
import requests
from datetime import datetime

 # 获取今天的日期
today_date = datetime.now().strftime('%Y-%m-%d')

# 1. 读取JSON文件
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# 2. 构造分析提示词
def build_prompt(item):
    return f"""请分析以下CSGO饰品数据并生成小红书爆款文案：
{json.dumps(item, ensure_ascii=False, indent=2)}

要求：
1. 突出近期价格变化（例如7天涨幅{item['items'][0]['饰品涨幅']['7']*100:.1f}%和30天涨幅{item['items'][0]['饰品涨幅']['30']*100:.1f}%）
2. 强调出租收益（例如短租年化{item['items'][0]['短租年化']:.1f}%）和出租热度）
3. 使用🔥等表情符号和#CSGO饰品 #游戏理财 等话题标签
4. 包含专业数据支撑的购买理由
5. 保持口语化、年轻化的表达风格
6. 请对比json中十款饰品的优势与劣势，并根据优势给出五款推荐的饰品并提供购买建议
7. 在文章最后给出提示，市场价格波动较大，本文仅供参考，实际购买请谨慎
8. 请为我生成一个爆款标题，围绕CS2千战饰品推荐进行展开
"""

def build_preset():
    return f"""角色：'你是一名专业的CSGO饰品分析师' '背景'：'你精通CSGO饰品市场，擅长撰写爆款小红书文案' '要求'：'你能够根据饰品数据生成小红书爆款文案'

"""

# 3. 调用Deepseek API
def get_deepseek_response(preset, prompt, api_key):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = json.dumps({
        "messages": [
            {
                "content": preset, 
                "role": "system"
            },
            {
                "content": prompt,
                "role": "user"
            }
        ],
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=100)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"请求失败：{str(e)}")
        raise e
    return response.json()['choices'][0]['message']['content']

# 4. 保存文案文件
def save_copywriting(content):

    filename = f"小红书_推广文案_千战系列" + today_date + ".txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"文案已保存至：{filename}")

# 主流程
def main():
    # 配置参数
    API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量获取API密钥
   
    # 在文件名后加上今天的日期
    JSON_FILE = f'goods_{today_date}.json'
    
    # 读取数据
    items = read_json_file(JSON_FILE)
    
    print(f"正在处理：{JSON_FILE}")
    
    # 构造提示词
    prompt = build_prompt(items)
    preset = build_preset(prompt)
    
    # 获取AI响应
    try:
        response = get_deepseek_response(preset, prompt, API_KEY)
        save_copywriting(response)
    except Exception as e:
        print(f"处理失败：{str(e)}")

if __name__ == "__main__":
    main()