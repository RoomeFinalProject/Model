import os
import pinecone
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore

# llamaindex 또한 3.5 turbo가 default

def my_chatbot(prompt):
    
    #key값 불러오기
    os.environ["OPENAI_API_KEY"] = get_openai_key()
    os.environ["PINECONE_API_KEY"] = get_pinecone_key()
    os.environ["PINECONE_ENV"] = get_pinecone_env()
    index_name = "openai"
    environment = get_pinecone_env()
    pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())

    # Pinecone DB에 Index를 연결
    pinecone_index = pinecone.Index("openai")
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine_chat = index.as_chat_engine()
    response_chat = query_engine_chat.chat(prompt)
    # query_engine = index.as_query_engine()
    # response_query = query_engine.query()
    # print('query',str(response_query))
    # print('chat',str(response_chat))

    return print(str(response_chat))

if __name__ == "__main__":
    # This block will be executed only if the script is run as the main program
    while True:
        text_input = input("User: ")
        if text_input == "exit":
            break
        my_chatbot(text_input)
    #my_chatbot('하반기 파생 결합증권 시장 동향에 대해 100글자로 요약해줘')
    