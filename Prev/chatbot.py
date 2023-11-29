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

# llamaindex 또한 3.5 turbo가 default
environment = get_pinecone_env()
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()

index_name = "openai"
#pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())

# Pinecone DB에 Index를 연결
pinecone_index = pinecone.Index("openai")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine()
query_engine_chat = index.as_chat_engine()

# response_query = query_engine.query() # 속도가 너무 느리다
# print('query',str(response_query))
response_chat = query_engine_chat.chat('2023년 하반기 파생 결합증권시장에 대해 3 줄로 요약해줘') # 속도가 너무 느리다
print('chat',str(response_chat))

'''
$ c:/Users/USER/Desktop/FinalProject/Model/venv_chatbot/Scripts/python.exe c:/Users/USER/Desktop/FinalProject/Model/chatbot.py
chat 2023년 하반기 파생 결합증권시장은 다음과 같은 특징을 가질 것으로 예상됩니다:

1. 주가연계 파생결합증권 중심: 주가연계 파생결합증권이 주요한 상품으로 부상할 것으로 예상됩니다. 이는 상환 후 재투자의 가능성이 높아지는 특징
을 가지고 있습니다.

2. 시장금리의 영향: 장기적으로 시장금리가 상승하는 상황이 지속될 경우, 할인율 부담으로 인해 기술주의 반등탄력은 낮아질 수 있습니다.

3. 비주권연계 파생결합증권의 투자 수요: 금리의 하락 가능성이 높아질수록 비주권연계 파생결합증권에 대한 투자 수요가 증가할 것으로 예상됩니다. 

4. 경쟁력의 회복: 파생결합증권의 경쟁력이 회복될 가능성이 높습니다.

5. 신용위험연계 파생결합증권의 투자 수요: 국공채 또는 우량 회사채 중심으로 자본차익거래를 할 수 있는 신용위험연계 파생결합증권에 대한 투자 수
요가 점진적으로 호전될 것으로 예상됩니다.
(venv_chatbot) 
'''