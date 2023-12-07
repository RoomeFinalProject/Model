설정 순서
1.1 가상환경 만들기 - python -m venv venv_chatbot

1.2 gitignore 설정 - .gitignore 파일 생성

1.3 requirements.txt - 필요한 pip을 install 해준다. - pip freeze > requirements.txt

1.4 git 연결 - git remote에 branch 생성: 여기서는 'chatbot' - git remote add origin https://github.com/RoomeFinalProject/Model.git - git branch --set-upstream-to=origin/chatbot main - 작동하지 않으면 - git ls-remote --heads origin (remote에 branch가 잘 생겼는지 확인 후) - git fetch - branch 간 잘 연결되어 있는지 확인 - git branch -vv - git pull 취소 - git reset --hard HEAD@{1}

2.1 크롤링 파일 설명 (JJ형 필독!) - crawlingTest.py 는 크롤링기초테스트 파일, 삭제해도 상관없음 - selenium_todayResearch.py 는 실행시 오늘올라온 리포트만 research_daily 에 저장됨 - selenium_TopRank.py 는 실행시 조회수 상위 리포트의 자료가 research_ranktop에 저장됨

2.2. 크게 4단계로 구성됨 - 1) 모듈임포트 - 2) while 구문 - 2.1) url 뽑아서 자료이름 저장하기 - 2.2) 다음버튼, 혹은 다른 버튼 클릭 후 적용하기
