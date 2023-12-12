from openai import OpenAI, AsyncOpenAI
from access import get_openai_key, get_pinecone_key, get_pinecone_env
import json

client = OpenAI(api_key = get_openai_key())
#print(get_openai_key())

text = ['벡터화 샘플 문장입니다', '이 것은 테스트 문장 입니다.']
def gpt_embedding(text):
    response = client.embeddings.create(
        model = 'text-embedding-ada-002',
        input = text
    )
    return response.data[0].embedding

res = gpt_embedding(text)

embeds = [res[i] for i in range(len(res))]
print(embeds)
print(len(embeds)) #1536
