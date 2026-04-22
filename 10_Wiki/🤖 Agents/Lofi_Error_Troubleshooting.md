---
id: LOFI-ERROR-REPORT-1.0
aliases: [로파이 에러 보고서, 커버 이미지 룰 위반, 로파이 환각 제어]
category: "[[10_Wiki/🤖 Agents]]"
confidence_score: 1.0
tags: [agent, lofi, troubleshooting, hallucination, prompt-engineering, music-generation]
last_reinforced: 2026-04-22
github_commit: "b51c206"
---

# [[로파이 에이전트 커버 이미지 및 규칙 위반 에러 분석]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> LLM의 컨텍스트 망각, 과거 지식 편향, 그리고 장르 키워드 환각으로 인한 에이전트 독단적 오류를 제어하기 위해, 강제 읽기 프로토콜(Init)과 프롬프트 통제 파이프라인을 도입한 아키텍처 개선안.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 스테이트리스(Stateless) 극복, 프롬프트 파이프라인 강제 변수화, 기존 상태(State) 선행 검증 로직 추가, AI 편향성 제어(장르 환각 억제).
- **발생한 에러 케이스 (Error Logs):**
  1. **인터뷰 대기 원칙 위반:** 사용자 답변 대기 전 선제적 이미지 생성 강행.
  2. **포맷 규칙 위반:** 16:9 렌더링 상황에서 1:1 API 호출.
  3. **영역 침범 (Scope Violation):** 할당된 채널 폴더 외부에서의 행동.
  4. **디자인 Core 룰 망각:** 실사 100%, 인물 금지, 일렉트릭 기타 필수 배치 누락.
  5. **과거 지식(Old Knowledge) 편향:** 쇼츠가 최대 60초라는 구형 데이터가 개입하여, 명시된 150초 규칙을 무시하고 60초짜리 BGM 코드를 하드코딩.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 단순히 `SKILL.md`에 글로 적어둔다고 해서 LLM이 항상 준수하는 것은 아님. 특히 구형 지식이 강할 경우 명시적 룰을 덮어씌우는 환각 현상 발생.
- **정책 변화 (Architecture Update):** 
  1. **강제 초기화(Init) 프로세스:** 행동 개시 전 무조건 `view_file`로 `SKILL.md`와 `LESSONS_LEARNED.md`를 소리내어(로그로) 복기하도록 시스템 뼈대 수정 🧠.
  2. **에러 주입 (Error Injection):** 초기 복기 절차를 무시할 시 진행을 차단하고 오답노트 요약을 강제 🧠.
  3. **프롬프트 템플릿 자유도 박탈:** 이미지 생성 시 에이전트의 재량을 없애고, `[Photorealistic, no humans, empty scene, featuring a detailed electric guitar, {변수}]` 형태의 강제 파이프라인 도입 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[Lofi_Agent_Project]]
- **Related:** [[LLM_Context_Window]], [[Prompt_Engineering_Architecture]]
- **Raw Source:** `[[00_Raw/로파이-error.md]]`
