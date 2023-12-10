import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from llama_index import SimpleDirectoryReader

from llama_index.llms import OpenAI
from llama_index.text_splitter import TokenTextSplitter
from llama_index.extractors import SummaryExtractor, QuestionsAnsweredExtractor, TitleExtractor, KeywordExtractor, EntityExtractor, BaseExtractor
from llama_index.ingestion import IngestionPipeline
import nest_asyncio
nest_asyncio.apply()

class Docs2Nodes:
    def __init__(self):
        # key값 불러오기
        os.environ["OPENAI_API_KEY"] = get_openai_key()

    def data_loader(self, path):
        filename_fn = lambda filename: {"file_name": filename}
        documents = SimpleDirectoryReader(path, file_metadata=filename_fn).load_data()
        return documents

    def docs2nodes(self, documents, llm, chunk_size=512, chunk_overlap=128):
        '''
            default 값: chunk_size = 512, chunk_overlap = 128
        '''
        text_splitter = TokenTextSplitter(separator=" ", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
         # sentenssesplitter와 차이는? SentenceSplitter(chunk_size=512, # include_extra_info=False, <-- 이게 있으면 에러난다. include_prev_next_rel=False)
        extractors = [
            TitleExtractor(nodes=5, llm=llm),
            #QuestionsAnsweredExtractor(questions=3, llm=llm),
            # EntityExtractor(prediction_threshold=0.5),
            SummaryExtractor(summaries=["prev", "self"], llm=llm),
            # KeywordExtractor(keywords=10, llm=llm),
            # CustomExtractor()
        ]
        transformations = [text_splitter] + extractors #Extractor는 원하는 함수를 만들어 넣을 수도 있다.
        pipeline = IngestionPipeline(transformations=transformations)
        documents_nodes = pipeline.run(documents=documents)
        return documents_nodes

llm = OpenAI(temperature=0, model="gpt-3.5-turbo")

if __name__ == "__main__":
    docs2nodes_instance = Docs2Nodes()
    path = "./data/research_youtube"
    documents = docs2nodes_instance.data_loader(path)
    documents_nodes = docs2nodes_instance.docs2nodes(documents, llm)
    print(len(documents_nodes))
    print('===========================================================')
    print(documents_nodes[20])
    print('===========================================================')
    print('text node. text:', documents_nodes[20].text)
    print('===========================================================')
    print('text node. metadata:', documents_nodes[20].metadata)
