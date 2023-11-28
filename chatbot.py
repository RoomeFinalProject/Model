import os
import pinecone
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from llama_index import (
    VectorStoreIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
)
from llama_index.vector_stores import PineconeVectorStore

# 저장시 필요한 env, key, index 정보
environment = get_pinecone_env()
index_name = "openai"
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()

pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())

# Pinecone DB에 Index를 연결
pinecone_index = pinecone.Index("openai")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
query_engine_chat = index.as_chat_engine()

response_query = query_engine.query("23년 파생결합증권시장의 전망에 대해 설명해줘") # 속도가 너무 느리다
print('query',str(response_query))
response_chat = query_engine_chat.chat("23년 파생결합증권시장의 전망에 대해 설명해줘") # 속도가 너무 느리다
print('chat',str(response_chat))