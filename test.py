'''
Author: yeffky
Date: 2025-02-10 12:57:11
LastEditTime: 2025-02-19 15:53:55
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

# import requests
# import json
# import os

# url = "https://api.deepseek.com/chat/completions"

# payload = json.dumps({
#   "messages": [
#     {
#       "content": "You are a helpful assistant",
#       "role": "system"
#     },
#     {
#       "content": "Hi",
#       "role": "user"
#     }
#   ],
#   "model": "deepseek-reasoner",
#   "frequency_penalty": 0,
#   "max_tokens": 2048,
#   "presence_penalty": 0,
#   "response_format": {
#     "type": "text"
#   },
#   "stop": None,
#   "stream": False,
#   "stream_options": None,
#   "temperature": 1,
#   "top_p": 1,
#   "tools": None,
#   "tool_choice": "none",
#   "logprobs": False,
#   "top_logprobs": None
# })
# API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量获取API密钥
# print(API_KEY)
# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json',
#   'Authorization': f'Bearer {API_KEY}'
# }

# response = requests.post(url, headers=headers, data=payload)

# print(response.json())

# from transformers import AutoTokenizer
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # 从 Hugging Face 加载一个标记器
# tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

# # 创建文本分割器
# text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
#     tokenizer,
#     chunk_size=256,
#     chunk_overlap=0,
#     separators=['---']
# )

# # 示例文本
# text = open('./xiaohongshu_drafts/小红书_推广文案_千战系列2025-02-17.txt', 'r', encoding='utf-8').read()

# # 使用文本分割器分割文本
# chunks = text_splitter.split_text(text)

# # 打印分割后的文本块
# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i + 1}:")
#     print(chunk)
#     print("-" * 50)

import requests

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    "messages": [
        {
            "role": "user",
            "content": "中国大模型行业2025年将会迎来哪些机遇和挑战？"
        }
    ],
    "stream": False,
    "max_tokens": 512,
    "stop": ["null"],
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {"type": "text"},
}
headers = {
    "Authorization": "Bearer sk-tibvwmdsduumotfvxzmxnneqrqjimsoqzbgehteeencevlht",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)