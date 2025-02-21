'''
Author: yeffky
Date: 2025-02-12 13:29:31
LastEditTime: 2025-02-19 13:55:28
'''
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer
from langchain.schema import Document
import time
import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com/'

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            process_new_file(file_path)  # 处理新文件
            print(f"新增文件已加载: {file_path}")

def process_new_file(file_path):
    # 加载文档（假设为txt格式）
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    print(type(documents[0]))

    # 从 Hugging Face 加载一个标记器
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=256,
        chunk_overlap=0,
        separators=['---']
    )
    # 进行文本分块
    text_chunks = text_splitter.split_text(documents[0].page_content)
    # 将分块结果转换为文档对象列表
    chunk_docs = [Document(page_content=chunk) for chunk in text_chunks]

    # 向量化并更新索引
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-zh")
    vector_store_dir = "./vector_store"
    if os.path.exists(vector_store_dir):
        vector_store = FAISS.load_local(vector_store_dir, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(chunk_docs)
    else:
        vector_store = FAISS.from_documents(chunk_docs, embeddings)
    vector_store.save_local(vector_store_dir)
    
def start_observer():
    observer = Observer()
    observer.schedule(NewFileHandler(), path="./xiaohongshu_drafts", recursive=False)
    observer.start()
    try:
        while True:
        # 每隔一小时检查一次
            time.sleep(1)
    except KeyboardInterrupt:
        # 当用户按下 Ctrl+C 时，停止观察者
        observer.stop()
    # 等待观察者线程结束
    observer.join()
    
if __name__ == "__main__":
    start_observer()