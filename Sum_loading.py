import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from llama_index import SimpleDirectoryReader

# 1. Key값 설정
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_ENV"] = get_pinecone_env()
environment = get_pinecone_env()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()

# 2. Data Loading
def list_files(directory):
    files = os.listdir(directory)
    return files

directory_path = '.\\data\\research_youtube'
file_names = list_files(directory_path)

#for file_name in file_names:
#    print(file_name)

import os

directory_path = ".\\data\\research_youtube"

def create_finance_docs(file_names, directory_path):
    filename_fn = lambda filename: {'file_name': filename}
    finance_docs = []

    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        documents = SimpleDirectoryReader(
            input_files=[file_path], file_metadata=filename_fn).load_data()
        documents[0].doc_id = file_name
        finance_docs.extend(documents)

    return finance_docs

    
#if __name__ == "__main__":
    
directory_path = '.\\data\\research_youtube'
file_names = list_files(directory_path)

directory_path = ".\\data\\research_youtube"
finance_docs = create_finance_docs(file_names, directory_path)
