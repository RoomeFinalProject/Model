설정 순서
1.1 가상환경 만들기 - python -m venv venv_chatbot

1.2 gitignore 설정 - .gitignore 파일 생성

1.3 requirements.txt - 필요한 pip을 install 해준다. - pip freeze > requirements.txt

1.4 git 연결 - git remote에 branch 생성: 여기서는 'chatbot' - git remote add origin https://github.com/RoomeFinalProject/Model.git - git branch --set-upstream-to=origin/chatbot main - 작동하지 않으면 - git ls-remote --heads origin (remote에 branch가 잘 생겼는지 확인 후) - git fetch - branch 간 잘 연결되어 있는지 확인 - git branch -vv - git pull 취소 - git reset --hard HEAD@{1}

2. 실행할때 access_key.json을 생성후  
   "OPENAI_API_KEY": ,
   "PINECONE_KEY": ,
   "PINECONE_ENV": ,
   를 만들어서 시행하면 된다.
