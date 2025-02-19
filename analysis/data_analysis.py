'''
Author: yeffky
Date: 2025-02-11 11:17:04
LastEditTime: 2025-02-19 16:08:42
'''
import json
import os
import requests
from datetime import datetime
import random
from langchain import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com/'

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
**根据以下文案风格，做出创新**：
    {selected_docs}

**注意**：
    - 在结尾加入提示，数据截至当前日期：{today_date}
    - 每一段内容使用 --- 进行分割
"""

def build_preset():
    with open('./docs/preset.txt', 'r', encoding='utf-8') as f:
        preset = f.read()
    # 创建文本嵌入对象
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh")
    print("embeddings加载完毕")
    # 检索知识库（扩大检索范围）
    vector_store = FAISS.load_local("./vector_store", embeddings, allow_dangerous_deserialization=True)
    retrieved_docs = vector_store.similarity_search(topic, k=5)  # 检索Top 5
    
    # 随机选择3个不同风格的参考文案
    random.shuffle(retrieved_docs)
    selected_docs = retrieved_docs[:3]

    preset += f"""\n **主题**：{topic}
    
    **创新要求**：
    - 使用{random.choice(["轻松幽默", "专业严谨", "犀利吐槽"])}的语气
    - 加入{["emoji表情", "热门梗", "互动提问"]}元素
    - 请不要出现除了中英文之外的语言
    """
    
    print(preset)
    return preset

# 3. 调用Deepseek API
def get_deepseek_response(preset, prompt, api_key):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        'Content-Type': 'application/json',
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
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "n": 1,
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        # 硅基流动不适用字段
        # "tools": None,
        # "tool_choice": "none",
        # "logprobs": False,
        # "top_logprobs": None
    })
    response = None
    while not response:
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=100)
            # response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            if not response.json():
                response = None
                print("没有收到响应，重试中...")
            else:
                print("收到响应，内容为：\n" + response.json()['choices'][0]['message']['content'])
        except requests.exceptions.RequestException as e:
            print(f"请求失败：{str(e)}")
            response = None
    return response.json()['choices'][0]['message']['content']

# 4. 保存文案文件
def save_copywriting(content):
    base_path = f'./xiaohongshu_drafts/'
    filename = f"小红书_推广文案_千战系列" + today_date + ".txt"
    print(content)
    with open(base_path + filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"文案已保存至：{filename}")

# 主流程
def analysis_data():
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
    analysis_data()