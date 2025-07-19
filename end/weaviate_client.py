import os
import requests

WEAVIATE_URL = os.getenv('WEAVIATE_URL')  # 从环境变量读取

def weaviate_get(path):
    return requests.get(f"{WEAVIATE_URL}{path}")

def weaviate_post(path, payload):
    return requests.post(f"{WEAVIATE_URL}{path}", json=payload)

def weaviate_put(path, payload):
    return requests.put(f"{WEAVIATE_URL}{path}", json=payload)

def weaviate_delete(path):
    return requests.delete(f"{WEAVIATE_URL}{path}")
