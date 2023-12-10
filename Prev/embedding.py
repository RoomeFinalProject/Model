from openai import OpenAI
import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from Docs2nodes import document_dic
client = OpenAI()

#key값 불러오기
os.environ["OPENAI_API_KEY"] = get_openai_key()

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

embedding_dic = {}
for i in range(len(document_dic)):
  node = document_dic[i]['node']
  embedding_dic[i] = get_embedding(node)
  
print(len(embedding_dic), len(embedding_dic[0]))