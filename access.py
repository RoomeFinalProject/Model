import json
import os

def get_openai_key():
    try:
        key_path = "access_key.json"
        
        with open(key_path) as f:
            data = json.load(f)
        key = data["OPENAI_API_KEY"]
    except Exception:
        # AWS Lambda의 환경 변수
        key = os.environ["OPENAI_API_KEY"]
        
    return key

def get_pinecone_key():
    try:
        key_path = "access_key.json"
        
        with open(key_path) as f:
            data = json.load(f)

        key = data["PINECONE_KEY"]
    except Exception:
        # AWS Lambda의 환경 변수
        key = os.environ["PINECONE_KEY"]
        
    return key

def get_pinecone_env():
    try:
        key_path = "access_key.json"
        
        with open(key_path) as f:
            data = json.load(f)

        key = data["PINECONE_ENV"]
    except Exception:
        # AWS Lambda의 환경 변수
        key = os.environ["PINECONE_ENV"]
        
    return key