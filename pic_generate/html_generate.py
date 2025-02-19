'''
Author: yeffky
Date: 2025-02-14 08:43:28
LastEditTime: 2025-02-19 16:27:01
'''
import requests
import json
import os
from datetime import datetime 

def build_prompt(drafts):
    prompt = "根据下面的小红书文案，帮我生成一个html页面，包含小红书的封面（需要一个卡片状的封面，上面只需文案内容即可，需要吸引眼球），以及下方几个要点内容，要点内容和封面我希望制作成卡片形式，并且每一部分的div请为我附上属性id，id为'card1', 'card2', ...。要求符合小红书平台的图文要求规则以及平替风格，还要符合小红书平台的用户审美。回复只要给出代码即可，请不要添加多余表达" 
    return f"""{prompt} \n\n小红书文案：\n\n{drafts}"""


def get_deepseek_response(prompt, api_key):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    payload = json.dumps({
        "messages": [
            {
                "content": prompt,
                "role": "user"
            }
        ],
        "model": "deepseek-ai/DeepSeek-R1",
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
        # "tools": None,
        # "tool_choice": "none",
        # "logprobs": False,
        # "top_logprobs": None
    })
    response = None
    while not response:
        try:
            print("发送请求")
            response = requests.post(url, data=payload, headers=headers, timeout=200)
            response.raise_for_status()
            if not response.json():
                response = None
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{str(e)}，开始重试...")
            response = None
    return response.json()['choices'][0]['message']['content']

def generate_html():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    today = datetime.now().strftime("%Y-%m-%d")
    
    file_path = "./xiaohongshu_drafts/小红书_推广文案_千战系列" + today +".txt"
    drafts = open(file_path, "r", encoding="utf-8").read()
    prompt = build_prompt(drafts=drafts)
    
    response = get_deepseek_response(prompt, api_key)
    print(response)
    with open('./pic_generate/pic.html', 'w', encoding='utf-8') as f:
        f.write(response)