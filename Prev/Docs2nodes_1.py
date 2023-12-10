import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env

#key값 불러오기
os.environ["OPENAI_API_KEY"] = get_openai_key()

# Data Loading
from llama_index import SimpleDirectoryReader

filename_fn = lambda filename: {"file_name": filename}
documents = SimpleDirectoryReader(
    "./data/pdf", file_metadata=filename_fn
).load_data()

# Nodes 및 Metadata 생성
from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.extractors import SummaryExtractor, QuestionsAnsweredExtractor, TitleExtractor, KeywordExtractor, EntityExtractor, BaseExtractor
from llama_index.ingestion import IngestionPipeline
import nest_asyncio


nest_asyncio.apply()

# 1. text_splitting 방법 설정
text_splitter = TokenTextSplitter(separator = " ", chunk_size = 512, chunk_overlap = 128)
  # sentenssesplitter와 차이는? SentenceSplitter(chunk_size=512, # include_extra_info=False, <-- 이게 있으면 에러난다. include_prev_next_rel=False)

# 2. metadata로 추출할 조건 설정
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
extractors = [
    TitleExtractor(nodes=5, llm=llm),
    #QuestionsAnsweredExtractor(questions=3, llm=llm),
    # EntityExtractor(prediction_threshold=0.5),
    SummaryExtractor(summaries=["prev", "self"], llm=llm),
    # KeywordExtractor(keywords=10, llm=llm),
    # CustomExtractor()
]

# 3. 변환 조건들 리스트
transformations = [text_splitter] + extractors

''' Extractor는 원하는 함수를 만들어 넣을 수도 있다.
class CustomExtractor(BaseExtractor):
  def extract(self, nodes):
    metadata_list = [
        {
            "custom":(node.metadata["document_title"] + "\n" + node.metadata["excerpt_keywords"])
        }
        for node in nodes
    ]
    return metadata_list
'''
# 4. node로 변환
pipeline = IngestionPipeline(transformations = transformations)
documents_nodes = pipeline.run(documents = documents)

# text node만 추출
print(len(documents_nodes))
print('===========================================================')
print(documents_nodes[20])
print('===========================================================')
print('text node. text:', documents_nodes[20].text)
print('===========================================================')
print('text node. metadata:', documents_nodes[20].metadata)

# Text와 meatadata만 추출
document_dic = {}
for i, text in enumerate(range(len(documents_nodes))):
  node_dic = {}
  document_dic[i] = node_dic
  node_dic['node'] = documents_nodes[i].text
  node_dic['metadata'] = documents_nodes[i].metadata
print(len(document_dic))
#document_dic[393]
