import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env

import pinecone

from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore

from llama_index import (
    VectorStoreIndex,
    get_response_synthesizer,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor,KeywordNodePostprocessor
from llama_index.prompts import PromptTemplate

import time

# 1. Key값 설정
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_ENV"] = get_pinecone_env()
environment = get_pinecone_env()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()
pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())

# 2. LlammaIndex - Pinecone 연동
pinecone_index = pinecone.Index("openai")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store)

# 3. Querying Stage 조작: configure retriever, Configuring node postprocessors, configure response synthesizer
## 3.1 configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

## 3.2 Configuring node postprocessors
node_postprocessors = [SimilarityPostprocessor(similarity_cutoff=0.5)]

## 3.3 configure response synthesizer
#response_synthesizer = get_response_synthesizer(response_mode="tree_summarize",) #(streaming = True, response_mode="tree_summarize",)
response_synthesizer = get_response_synthesizer(response_mode="compact",) #(streaming = True, response_mode="tree_summarize",)
  #synth = get_response_synthesizer(text_qa_template=custom_qa_prompt, refine_template=custom_refine_prompt)
  # 이 함수를 사용하면 쉽게 prompt engineering을 할 수 있다.
  # 지금 streaming 기능이 작동하지 않음.
  # streaming = True -> response.response로 응답 할 수 없음
  # prompts_dict = query_engine.get_prompts() # (response_mode="compact") 일때
  # print(list(prompts_dict.keys()))
  
## 3.4 assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=node_postprocessors,
)

# 4. Prompt Engineering: shakespeare!
qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query in the style of a Shakespeare play.\n"
    "Use Korean"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_tmpl}
)

import time

def my_chatbot(text_input):
    start_time = time.time()
    response = query_engine.query(text_input)
    response_time = time.time() - start_time
    
    print("Response Time: {:.2f} seconds".format(response_time))
    print("Response:", response.response) # print("Response:", response.response) 이렇게 하면 에러 발생 ..
    # print("Metadata:", response.metadata.values())

# Example usage
#my_chatbot("안녕?")
