'''
Author: yeffky
Date: 2025-02-11 11:17:04
LastEditTime: 2025-02-12 17:38:40
'''
import json
import os
import requests
from datetime import datetime
import random
from langchain import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


 # 获取今天的日期
today_date = datetime.now().strftime('%Y-%m-%d')
topic = "CS2饰品"

# 1. 读取JSON文件
def read_json_file(filename):
    with open(f'data/{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)

# 2. 构造分析提示词
def build_prompt(item):
    with open('./docs/prompt.txt', 'r', encoding='utf-8') as f:
        prompt = f.read()
    # 创建文本嵌入对象
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh")
    # 检索知识库（扩大检索范围）
    vector_store = FAISS.load_local("./vector_store", embeddings, allow_dangerous_deserialization=True)
    retrieved_docs = vector_store.similarity_search(topic, k=5)  # 检索Top 5
    
    # 随机选择3个不同风格的参考文案
    random.shuffle(retrieved_docs)
    selected_docs = retrieved_docs[:3]
    
    return f"""{prompt}, 
{json.dumps(item, ensure_ascii=False, indent=2)} 
**避免重复以下风格，做出创新**：
    {selected_docs}
**创新要求**：
    - 使用{random.choice(["轻松幽默", "专业严谨", "犀利吐槽"])}的语气
    - 加入{["emoji表情", "热门梗", "互动提问"]}元素
"""

def build_preset():
    with open('./docs/preset.txt', 'r', encoding='utf-8') as f:
        preset = f.read()
    # 创建文本嵌入对象
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh")
    # 检索知识库（扩大检索范围）
    vector_store = FAISS.load_local("./vector_store", embeddings, allow_dangerous_deserialization=True)
    retrieved_docs = vector_store.similarity_search(topic, k=5)  # 检索Top 5
    
    # 随机选择3个不同风格的参考文案
    random.shuffle(retrieved_docs)
    selected_docs = retrieved_docs[:3]

    preset += f"""\n **主题**：{topic}
    
    **避免重复以下风格，做出创新**：
    {selected_docs}
    
    **创新要求**：
    - 使用{random.choice(["轻松幽默", "专业严谨", "犀利吐槽"])}的语气
    - 加入{["emoji表情", "热门梗", "互动提问"]}元素
    """
    
    print(preset)
    return preset

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
    response = None
    while not response:
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=100)
            response.raise_for_status()
            if not response.json():
                response = None
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{str(e)}")
            response = None
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
    preset = build_preset()
    
    # 获取AI响应
    try:
        response = get_deepseek_response(preset, prompt, API_KEY)
        save_copywriting(response)
    except Exception as e:
        print(f"处理失败：{str(e)}")

if __name__ == "__main__":
    main()