---
id: c3a8b2d1-4e7f-4c12-9f3a-8b1c4e7d5f2a
aliases: [Coupang MMS, 예곰 단문 메시지 생성기, 쿠팡 SMS 분할기]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 0.95
tags: [SMS_분할, 안심번호, 로컬AI, Ollama, gemma4, 웹개발, 바닐라JS, 아키텍처]
entities: [PER: 박상무/유부장/김대리/이과장/예곰, ORG: 쿠팡, TECH: HTML5/CSS3/Vanilla JS/Ollama/gemma4:e4b/Vercel/Python http.server/Windows Batch]
last_reinforced: 2026-05-07
github_commit: ""
---

# [[CoupangMMS Development History]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 쿠팡 안심번호 길이 제한 문제를 해결하기 위해, 로컬 AI(gemma4)와 순수 바닐라 JS를 결합하고 윈도우 배치 스크립트 기반의 독립적인 로컬 서버 구동 방식을 적용한 초경량 텍스트 자동 분할 및 검수 시스템.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 보안 제약(Mixed Content, CORS)을 우회하기 위해 웹 배포(Vercel) 대신 파이썬 내장 모듈(`http.server`)과 윈도우 `.bat` 스크립트를 활용하여 사용자 친화적인 원클릭 로컬 실행 환경을 구축함.
- **세부 내용:**
  - **스마트 분할:** 80 Byte 한글(2byte)/영문(1byte) 실시간 계산 및 단어가 끊기지 않는 스마트 띄어쓰기 분할 로직 구현 (꼬리말 인덱스 포함).
  - **보안 및 아키텍처 전환:** Vercel 배포 시 발생하는 HTTPS/HTTP 혼합 콘텐츠 차단을 해결하기 위해 로컬 환경으로 과감히 전환. 
  - **파이썬 로컬 서버 도입:** `file://` 환경에서 외부 API 호출을 차단하는 샌드박스 이슈를 우회하고자, 파이썬 기반 임시 웹 서버(`127.0.0.1:8500`) 및 백그라운드 지연 실행 아키텍처 적용.
  - **AI 연동 고도화:** 세컨컴의 `gemma4:e4b` 모델과 연동하여 비즈니스 문구 교정. 무거운 모델의 로딩 타임을 버티기 위해 Fetch API 타임아웃을 60초(60000ms)로 상향.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- **로컬 기반 AI 도구 파이프라인의 완성:** 브라우저 보안 제약으로 외부 로컬 AI 서버와의 통신이 막혔을 때, 가장 단순한 파이썬 서버와 윈도우 배치 스크립트 조합으로 문제를 해결하는 패턴입니다. 이는 향후 복잡한 백엔드 없이 세컨컴 AI를 적극적으로 활용하는 모든 사내 유틸리티 툴 개발의 '표준 경량 아키텍처'로 확장될 수 있습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 없음.
- **정책 변화:** 웹 애플리케이션이라고 해서 무조건 Vercel 등의 외부 호스팅을 고집할 필요가 없음을 증명. 로컬 하드웨어(세컨컴 AI)와의 시너지가 필요할 때는 '로컬 기반 독립 실행 아키텍처'가 오히려 더 높은 가치를 지님. (관련 가중치 업데이트 🧠)

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects]]
- **Related:** [[Local AI Architecture]], [[Ollama API Integration]], [[Windows Batch Automation]]
- **Raw Source:** [[99_Archive/Raw_Backup/[AWIKI_DONE]_CoupangMMS_Development_History.md]]
