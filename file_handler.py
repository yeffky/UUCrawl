'''
Author: yeffky
Date: 2025-02-12 13:29:31
LastEditTime: 2025-02-14 11:20:18
'''
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer
from langchain.schema import Document
from text2vec import SentenceModel

import os


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

    headers_to_split_on = [("###", "Header"), ("####", "SubHeader")]
    # 从 Hugging Face 加载一个标记器
    tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=1000,
        chunk_overlap=0,
        separators=[header[0] for header in headers_to_split_on]
    )
    # 进行文本分块
    text_chunks = text_splitter.split_text(documents[0].page_content)
    # 将分块结果转换为文档对象列表
    chunk_docs = [Document(page_content=chunk) for chunk in text_chunks]

    # 向量化并更新索引
    embeddings = SentenceModel('shibing624/text2vec-base-chinese')
    vector_store_dir = "./vector_store"
    if os.path.exists(vector_store_dir):
        vector_store = FAISS.load_local(vector_store_dir, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(chunk_docs)
    else:
        vector_store = FAISS.from_documents(chunk_docs, embeddings)
    vector_store.save_local(vector_store_dir)
    
import time

observer = Observer()
observer.schedule(NewFileHandler(), path="./xiaohongshu_drafts", recursive=False)
observer.start()
try:
    while True:
    # 每隔 1 秒检查一次
        time.sleep(1)
except KeyboardInterrupt:
    # 当用户按下 Ctrl+C 时，停止观察者
    observer.stop()
# 等待观察者线程结束
observer.join()