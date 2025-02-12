'''
Author: yeffky
Date: 2025-02-10 12:57:11
LastEditTime: 2025-02-11 18:48:44
'''
# import hashlib
# import time

# def le(e):
#     # 第一次MD5，将输入转换为字符串并计算MD5
#     first_md5 = hashlib.md5(str(e).encode()).hexdigest()
#     # 拼接字符串并第二次计算MD5
#     combined = first_md5
#     second_md5 = hashlib.md5(combined.encode()).hexdigest()
#     return second_md5

# # 获取当前时间的毫秒级时间戳（与JavaScript的new Date().getTime()等效）
# t = int(time.time() * 1000)
# # 计算最终结果
# o = le(t)

# print("Timestamp:", t)
# print("Result:", o)

import requests
import json
import os

url = "https://api.deepseek.com/chat/completions"

payload = json.dumps({
  "messages": [
    {
      "content": "You are a helpful assistant",
      "role": "system"
    },
    {
      "content": "Hi",
      "role": "user"
    }
  ],
  "model": "deepseek-reasoner",
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
API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量获取API密钥
print(API_KEY)
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {API_KEY}'
}

response = requests.post(url, headers=headers, data=payload)

print(response.json())