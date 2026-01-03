# 🌙 심야톡방 NightTalk

## AI-Agent 소개

- 본 AI-Agent는 익명 커뮤니티 서비스에서 발생할 수 있는
불법·유해 게시물(마약 거래, 성인 사이트 광고, 도박 사이트 광고 등)을 자동으로 탐지하고
블라인드 처리하기 위해 구현된 모더레이션 전용 서비스입니다.

- vLLM 기반 LLM 추론 서버를 사용하여 고속 추론 환경을 구성했으며
- Qwen3 4B 오픈 파라미터 모델을 활용해 게시글 텍스트를 분석합니다.
- 메인 백엔드와 분리된 독립 Agent 마이크로서비스로 설계되었습니다.

### 개발 인원 및 기간

- 개발기간 :  2025-11-03 ~ 2025-12-07
- 개발 인원 : 프론트엔드/백엔드/AI 1명 (본인)

### 사용 기술 및 tools
- LLM Inference : vLLM
- Model : Qwen3-4B-Instruct-2507 (Open Parameter)
- Backend API : FastAPI
- Infra :  Docker, AWS EC2(NVIDIA A10 GPU)

### Front-end
- <a href="https://github.com/kim-min-min/ktb_community_frontend">Front-end Github</a>

### Back-end
- <a href="https://github.com/kim-min-min/ktb_community_backend">Back-end Github</a>


### 폴더 구조
<details>
  <summary>폴더 구조 보기/숨기기</summary>
  <div markdown="1">

      ktb_community_agent
      ├── app
      │   ├── agent
      │   │   ├── moderation_agent.py   
      │   │   ├── prompt.py             
      │   │   └── tools.py             
      │   │
      │   ├── routers
      │   │   └── moderation.py         
      │   │
      │   ├── schemas.py                
      │   └── main.py                   
      │
      ├── Dockerfile                    
      ├── Docker-compose-agent.yml      
      ├── requirements.txt              
      ├── .env                          
      ├── .gitignore
      └── .dockerignore


  </div>
  </details>
  <br/>

## 동작 흐름
- 사용자가 게시글 또는 댓글 작성
- 메인 백엔드에서 게시글 저장
- AI-Agent로 모더레이션 요청 전송
- Agent가 LLM 추론을 통해 불법/유해 여부 판단
- 불법성이 높은 게시글은 자동 블라인드 처리




## 트러블 슈팅

- vLLM 기반 GPU 추론 환경 구성 과정의 어려움

- 문제
--오픈 파라미터 LLM(Qwen3-4B)을 다운로드한 뒤
vLLM으로 GPU 추론 서버를 구성하는 과정에서
단순 모델 실행이 아닌 컨테이너 기반 GPU 추론 환경 설정이 필요했습니다

- 원인

기본 Docker 환경에서는 GPU 사용이 불가능

NVIDIA 드라이버, Container Toolkit, Docker runtime 설정이 올바르게 연결되지 않음

- 해결

NVIDIA Container Toolkit을 설치하여 Docker에서 GPU 사용 가능하도록 환경 구성

Docker runtime에 NVIDIA GPU를 명시적으로 등록

GPU 인식 여부를 컨테이너 내부에서 직접 검증한 후 vLLM 서버 배포

- 결과

vLLM 기반 GPU 추론 서버를 안정적으로 실행

오픈 파라미터 모델을 실제 운영 환경에서 활용 가능한 형태로 배포

이후 Agent 서비스와 연동하여 실시간 모더레이션 처리 가능

<br/>

## 프로젝트 후기
- 이번 프로젝트를 통해
LLM을 단순 실험용 모델이 아닌, 실제 서비스에서 동작하는 운영 컴포넌트로 구성·배포하는 경험을 할 수 있었습니다.

특히,

vLLM 기반 GPU 추론 환경을 직접 구성하며 LLM 인프라 이해도 향상

메인 백엔드와 분리된 Agent 아키텍처를 설계하여 서비스 안정성 확보

불법 게시물 자동 차단이라는 명확한 운영 목적을 가진 AI 기능 구현

을 경험하며
LLM 모델·추론 서버·백엔드 서비스가 어떻게 유기적으로 연결되는지에 대한 이해를 크게 확장할 수 있었습니다.

- 향후에는,

탐지 카테고리 세분화

오탐/미탐 로그 기반 정책 및 프롬프트 고도화

관리자 검토(REVIEW) 단계 추가
등을 통해 Agent를 더욱 정교한 운영형 AI 서비스로 발전시킬 계획입니다.

등을 통해 Agent를 더욱 정교한 운영형 AI 서비스로 발전시킬 계획입니다.
<br/>
<br/>
<br/>
