---
id: b8c9d04f-3f5c-4b2e-c903-1c2d4e5f6b7c
aliases: [실행_누락, 실무_전가, 에이전트_환각, 사전_탐색_부재]
category: "[[10_Wiki/Troubleshooting/Agent_Errors]]"
confidence_score: 0.95
tags: [Troubleshooting, Agent_Hallucination, Park-SangMoo, Lofi, Automation]
entities: [PER: 박상무, PER: 로파이, PER: 설감사, ORG: Lo-fi Moment, TECH: list_dir, TECH: grep_search, TECH: run_command]
last_reinforced: 2026-04-27
github_commit: "Pending"
---

# [[에이전트 실행 누락 및 실무 전가 환각 분석]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 에이전트가 기존 자동화 스크립트의 존재를 무시하고 사용자에게 수동 작업을 전가하는 환각을 방지하려면, 지시 수행 전 반드시 로컬 파일 구조를 사전 탐색(`list_dir`)하도록 프롬프트 레벨에서 강제해야 한다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 박상무와 로파이 에이전트가 `e:\Lo-fi Moment\` 내에 구축된 자동화 파이프라인(`music_generator.py` 등)이 존재함에도, 이를 탐색하지 않고 외부 API 부재 등을 이유로 사용자에게 수동 프롬프트 복붙 등을 요구하는 '실무 전가' 오류 발생.
- **세부 내용:**
  - **오류 증상:** 기존 정상 작동하던 렌더링/생성 코드를 무시하고 실행 누락.
  - **문제 원인 (Root Cause):** 새로운 지시를 받았을 때 현재 디렉토리의 파일 구조를 탐색하여 기존 스크립트를 검증하라는 탈출 조건(Exit Condition) 부재로 인한 환각(Hallucination).
  - **해결 방안 (Prompt Patch):** 모든 에이전트 규칙에 "수동 개입 요구 전, 반드시 `list_dir` 등으로 현재 작업 폴더를 리스팅하여 기존 자동화 스크립트 존재 여부를 검증하라"는 수칙 강제 추가.
  - **긴급 조치:** 중단된 파이프라인 복구를 위해 사용자가 열어둔 `temp_render.py` 등을 `run_command`로 즉시 실행.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 단순히 에러를 고치는 것을 넘어, 에이전트들이 "내가 할 수 없는 일"이라고 속단하기 전에 "시스템에 구축된 도구(스크립트)가 있는가?"를 먼저 탐색하게 만드는 **'자원 확인 우선(Resource-First Check)'** 프로토콜로 확장 가능. 이는 향후 새로운 에이전트가 투입되더라도 로컬 환경의 자산을 최대한 활용하는 자생적 생태계 구축의 기반이 됨.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** LLM의 고질적인 한계인 "할 수 없습니다"라는 답변을, 외부 API 제약에만 맞추어 생각했으나, 로컬 스크립트 탐색 부재가 낳은 환각임이 확인됨.
- **정책 변화:** 
  - `list_dir` 및 `grep_search` 도구 활용을 에이전트 행동 수칙의 0순위(Init 단계 다음)로 격상.
  - 1인 기업가 대표님께 수동 실무를 전가하는 에이전트 행동 패턴에 대한 강력한 페널티 부여 및 통제 강화.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/Troubleshooting/Agent_Errors]]
- **Related:** [[로파이: 에이전트 룰 무시 및 컨텍스트 망각 에러 분석]], [[10_Wiki/System_Policy/Agent_Rules/Agent_Room_Management_Policy]]
- **Raw Source:** [[00_Raw/agent-error-fix Lo-fi Moment.md]]
