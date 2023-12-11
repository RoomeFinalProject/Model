from llama_index import ServiceContext, get_response_synthesizer
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI
import nest_asyncio
import os
from access import get_openai_key, get_pinecone_key, get_pinecone_env
from Sum_loading import file_names, finance_docs
from Sum_2JSONFormat import convert_to_jsonformat

# 1. Key값 설정
os.environ["OPENAI_API_KEY"] = get_openai_key()
os.environ["PINECONE_ENV"] = get_pinecone_env()
environment = get_pinecone_env()
os.environ["PINECONE_API_KEY"] = get_pinecone_key()
nest_asyncio.apply()

# LLM (gpt-3.5-turbo)
chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

from llama_index.prompts import PromptTemplate
qa_prompt_tmpl = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "Summarize only Korean"
    "Summarize over 500 characters."
    "Answer with Korean"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt = PromptTemplate(qa_prompt_tmpl)

# default mode of building the index
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", summary_template=qa_prompt, use_async=True
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    finance_docs,
    service_context=service_context,
    response_synthesizer=response_synthesizer,
    show_progress=True,
)

#json_file_path = ".\\data\\Results_Summary"
for file_name in file_names:
  content = doc_summary_index.get_document_summary(f"{file_name}")
  json_result = convert_to_jsonformat(file_name, content)
  print(json_result)
  