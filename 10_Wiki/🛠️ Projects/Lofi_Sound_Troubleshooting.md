---
id: LOFI-TROUBLESHOOTING-01
aliases: [로파이 드럼 제거, NotebookLM RAG, 사운드 트러블슈팅]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 0.98
tags: [lo_fi, music_generation, notebooklm, rag, troubleshooting, prompt_engineering]
last_reinforced: 2026-04-24
github_commit: "31a40bb"
---

# [[Lo-fi Agent: NotebookLM 기반 드럼/퍼커션 개입 억제 (RAG)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> Lo-fi 채널의 고질적 문제인 '원치 않는 드럼/비트 사운드 개입'을 억제하기 위해, NotebookLM의 RAG 지식을 Lo-fi 에이전트의 프롬프트 엔지니어링에 직접 연동하는 트러블슈팅 방법론.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** AI 음악 생성기(Lyria 3 Pro 등)의 환각(불필요한 비트 추가)을 제어하기 위한 외부 지식 검색 증강(RAG) 도입.
- **세부 내용:**
  - **이슈 정의:** 순수 일렉트릭 기타/클래식 베이스의 Lo-fi 무드를 의도했으나, 생성 모델이 무작위로 드럼이나 퍼커션 사운드를 끼워 넣는 현상 발생.
  - **해결 접근법 (2026-04-24):** Lo-fi 에이전트에게 NotebookLM을 활용하도록 지시. 수많은 음악 이론과 프롬프트 공식 논문을 NotebookLM에 먹이고, '드럼 소리가 완전히 배제된 솔로 악기 연주'를 강제하는 최적의 Negative Prompt나 가중치 파라미터를 도출함.
  - **기대 효과:** 무의미한 렌더링 반복(리트라이 루프) 방지 및 토큰 비용 절감.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 단순 프롬프트 수정(예: "No drums")만으로는 생성기의 환각을 완벽히 통제할 수 없었음.
- **정책 변화:** 단순 프롬프트 수정을 넘어, NotebookLM에서 추출한 논문/문서 기반의 '지식 프롬프트'를 Lo-fi 에이전트의 System Prompt에 주입하는 방향으로 정책을 고도화함 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects/Lo-fi_Moment]]
- **Related:** [[NotebookLM_Lean_Architecture]], [[Lo-fi_Agent_Skills]]
- **Raw Source:** `[[00_Raw/sehyun.md#2026-04-24]]`
