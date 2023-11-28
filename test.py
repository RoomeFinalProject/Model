import json
import os
import pinecone
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from openai import OpenAI, AsyncOpenAI


pinecone.init(api_key = get_pinecone_key(), environment = get_pinecone_env())

# 모델 삭제를 위한 코드
# pinecone.delete_index('openai')
# print('Complete delete index')

# 모델의 토큰수 확인
os.environ["OPENAI_API_KEY"] = get_openai_key()
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])

text = ['백터화 샘플 문장 입니다.', '이 것은 테스트 문장입니다.']

def gpt_embedding( text ):
    reponse = client.embeddings.create(
        # 모델의 문장 최대 크기 : 1536 토큰으로 문장을 표현
        # 모델이 바뀌면 문장의 크기도(최대 토큰 사용량도) 다르다
        model = 'text-embedding-ada-002',
        input = text
    )
    return reponse.data[0].embedding

res = gpt_embedding( text )

embeds = [res[i] for i in range(len(res))]
print(len(embeds))
# 사용할 모델과 같은 차원으로 한다.

# Index 생성
if 'openai' not in pinecone.list_indexes():
    pinecone.create_index('openai', dimension=len(embeds))
index = pinecone.Index('openai')

print(f"{len(embeds)} 차원의 Index 생성")

