import pinecone
import os

from access import get_openai_key, get_pinecone_key, get_pinecone_env
from llama_index import (
    VectorStoreIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
)
from llama_index.vector_stores import PineconeVectorStore
from llama_index.llms import OpenAI

import logging
import sys

from pathlib import Path
from llama_index import download_loader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# Access
pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())


print(pinecone.Index("openai").describe_index_stats())

# load documents
PDFReader = download_loader("PDFReader")
loader = PDFReader()
PDF_documents = loader.load_data(file=Path('.\data\pdf\stocks_korean.pdf'))

# initialize without metadata filter
from llama_index.storage.storage_context import StorageContext

# 저장시 필요한 env, key, index 정보
environment = get_pinecone_env()
index_name = "openai"
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()

# Service_context 설정:
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")                         # llm = llm -> predict 모델에 llm을 적용하겠다!
service_context = ServiceContext.from_defaults(llm=llm, chunk_size = 1024) # chunk_size default = 1024

# 파인콘에서 벡터 저장소 (index) 설정
vector_store = PineconeVectorStore(
                                   index_name=index_name,
                                   environment=environment,
                                   #metadata_filters=metadata_filters,
                                   )
# 라마가 가져올 storage Index 설정: 여기서는 pinceone의 index로 설정되었다.
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# 라마인덱스에서 파이콘으로 데이터 업로드: 이 함수는 확인 필
text_index = VectorStoreIndex.from_documents(
                                             PDF_documents,
                                             storage_context=storage_context,
                                             service_context=service_context,
                                              )

print(pinecone.Index("openai").describe_index_stats())