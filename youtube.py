# 실행 python youtube.py
# 가상환경생성 python -m venv summary
# 가상환경실행 .\venv\Scripts\activate

import os
import logging
import sys
import llama_index
import openai
import json
from llama_index import SimpleDirectoryReader, Document, GPTVectorStoreIndex, LLMPredictor, ServiceContext, PromptHelper
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from google.oauth2 import service_account
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings.langchain import LangchainEmbedding

# 스크립트 파일이 위치한 디렉토리(상대경로 설정) = C:\\Users\\user\\Desktop\\Final_project\\Youtube_summary
script_directory = os.path.dirname(os.path.abspath(__file__))

# openAI key 획득
def get_openai_key(): 
    openai_key = None
    try:
        # openai_key_path = "C:\\Users\\user\\Desktop\\Final_project\\openai_key.json"
        openai_key_path = os.path.join(script_directory, '..', "openai_key.json")
        with open(openai_key_path) as f:
            data1 = json.load(f)
        openai_key = data1['OPENAI_API_KEY']
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {openai_key_path}")
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 오류: {e}")
    except KeyError:
        print("JSON 파일에서 'OPENAI_API_KEY' 키를 찾을 수 없습니다.")
    except Exception as e:
        print(f"예기치 않은 오류가 발생했습니다: {e}")
        
    # 파일에서 로드되지 않으면 환경 변수에서 시도합니다.
    if openai_key is None:
        try:
            openai_key = os.environ['OPENAI_API_KEY']
        except KeyError:
            print("'OPENAI_API_KEY' 환경 변수가 설정되어 있지 않습니다.")
    
    return openai_key

# OpenAI API 키 로드를 시도합니다.
api_key = get_openai_key()

if api_key is not None:
    # openai 모듈에 API 키를 설정합니다.
    openai.api_key = api_key
    print("OpenAI API 키가 성공적으로 로드되었습니다.")
else:
    print("OpenAI API 키를 로드하는 데 실패했습니다.")

# openai key 획득
def get_youtube_api_key(): 
    youtube_api_key = None
    try:
        # youtube_api_key_path = "C:\\Users\\user\\Desktop\\Final_project\\youtube_api_key.json"
        youtube_api_key_path = os.path.join(script_directory, '..',"youtube_api_key.json")
        with open(youtube_api_key_path) as f:
            data2 = json.load(f)
        youtube_api_key = data2['youtube_api_key']
    except Exception:
        # 로컬에서 파일을 읽지 못할 경우 또는 파일이 없는 경우
        # 다른 예외처리를 추가하여 필요에 따라 처리할 수 있습니다.
        pass
    return youtube_api_key

# youtube 객체 생성        
client_youtube = YouTubeTranscriptApi()

# 내부적으로 작동하는 로그 출력x
logging.basicConfig( stream=sys.stdout, level=logging.INFO, force=False)

# 서비스 계정 JSON 키 파일 경로
#service_account_file = "C:\\Users\\user\\Desktop\\Final_project\\youtube_api_key.json"
service_account_file = os.path.join(script_directory, '..',"youtube_api_key.json")

# 서비스 객체 생성
credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])
youtube = build("youtube", "v3", credentials=credentials)
    
def get_latest_video(api_key, channel_id):
    youtube = build("youtube", "v3", credentials=credentials)

    try:
        # 채널에서 최신 동영상의 ID를 가져오기
        channel_id = channel_id.split("/")[-1]  # URL에서 채널 ID 추출
        channel_response = youtube.channels().list(id=channel_id, part="contentDetails").execute()
        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # 업로드된 동영상 목록에서 최신 동영상의 ID를 가져오기
        playlist_response = youtube.playlistItems().list(           # playlistItems().list: youtube api 응답에서 최신동영상 ID 추출
            playlistId=uploads_playlist_id,                         # youtube api 응답에서 최신동영상 ID 추출
            part="snippet",
            maxResults=1                                            # 리스트의 첫번째 동영상이 최신 영상
        ).execute()                                                 # playlist_response["items"]: 해당 재생목록에 속한 동영상들의 목록들이 있음

        latest_video_id = playlist_response["items"][0]["snippet"]["resourceId"]["videoId"]

        # 최신 동영상의 상세 정보 가져오기
        video_response = youtube.videos().list(
            id=latest_video_id,
            part="snippet"
        ).execute()

        return latest_video_id, video_response["items"][0]["snippet"]["title"]

    except Exception as e:
        print(f"에러가 발생했습니다: {e}")
        return None, None

def get_korean_transcript(video_id, file_path):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        korean_text = " ".join(entry['text'] for entry in transcript)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(korean_text)

        return korean_text

    except Exception as e:
        print(f"자막을 가져오는 동안 에러가 발생했습니다: {e}")
        return None

    
# YouTube API 키와 채널 ID를 설정
channel_ids = [
    "https://www.youtube.com/channel/UCr7XsrSrvAn_WcU4kF99bbQ",     # 박곰희TV
    "https://www.youtube.com/channel/UCFznPlqnBtRKQhtkm6GGoRQ",     # 달팽이주식
    "https://youtube.com/channel/UCWeYU4snOLj4Jj52Q9VCcOg",         # 주식하는강이사
    "https://youtube.com/channel/UCw8pcmyPWGSik7bjJpeINlA",         # 기릿의 주식노트 Let's Get It
    "https://youtube.com/channel/UCM_HKYb6M9ZIAjosJfWS3Lw",         # 미주부
    "https://www.youtube.com/channel/UCv-spDeZBGYVUI9eGXGaLSg",     # 시윤주식
]
#base_path = "C:\\Users\\user\\Desktop\\Final_project\\Youtube_summary\\text_sample"
base_path = os.path.join(script_directory, "text_sample")

# 최신 동영상 가져오기
for i, channel_id in enumerate(channel_ids, start=1):
    latest_video_id, latest_video_title = get_latest_video(get_youtube_api_key(), channel_id)

    if latest_video_id:
        print("\nChannel ID:", channel_id)
        print("Latest Video Title:", latest_video_title)        # 영상 제목
        print("Latest Video ID:", latest_video_id)              # 영상 id

        # 영상의 한국어 자막 가져오기 및 저장
        file_path = f'{base_path}\\korean_transcript_{i}.txt'
        korean_transcript = get_korean_transcript(latest_video_id, file_path)

        if korean_transcript:
            print("Korean Transcript:")
            print(korean_transcript)
        else:
            print("No Korean transcript available.")

# 텍스트 경로 지정, documents 설정
#doc_dir = "C:\\Users\\user\\Desktop\\Final_project\\Youtube_summary\\text_sample"
doc_dir = os.path.join(script_directory, "text_sample")
documents = SimpleDirectoryReader(doc_dir).load_data()

# 인덱스(벡터디비) 생성
index = GPTVectorStoreIndex.from_documents(documents)

# 프롬프트기반 gpt모델(청크분할)
prompt_helper = PromptHelper(
    num_output=1024,              # LLM의 최대 출력 토큰수 조정(gpt3.5는 4096개가 최대치)
    chunk_overlap_ratio=0.1        # 10%비율로 오버랩 가능하게 조정
)

service_context = ServiceContext.from_defaults(
    prompt_helper=prompt_helper
)

index_prompt = GPTVectorStoreIndex.from_documents(
    documents,
    service_context=service_context
)

# 허깅페이스기반 임베딩모델
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
    model_name='sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens'
))

service_context = ServiceContext.from_defaults(
    embed_model=embed_model
)

index_embed = GPTVectorStoreIndex.from_documents(
    documents,
    service_context=service_context
)

for j, doc in enumerate(documents, start=1):
    selected_index = GPTVectorStoreIndex.from_documents([doc], service_context=ServiceContext.from_defaults(embed_model=embed_model))
    result = selected_index.as_query_engine().query(f'{j}번 텍스트의 내용을 Summarize the following in 10 bullet points.')
    print(f"{j}번 문서 요약 (Selected Model):\n{result}\n")