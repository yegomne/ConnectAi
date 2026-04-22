---
id: a7f8d93c-2e4b-4a1d-b892-0b1c9e3f4a5b
aliases: [로파이_오류, 에이전트_기억상실, 프롬프트_제어]
category: "[[10_Wiki/Troubleshooting/Agent_Errors]]"
confidence_score: 0.98
tags: [Troubleshooting, Agent_Memory, Lofi, Prompt_Engineering]
last_reinforced: 2026-04-21
github_commit: "Pending"
---

# [[로파이: 에이전트 룰 무시 및 컨텍스트 망각 에러 분석]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 에이전트의 '기억 상실(Stateless)'은 자연스러운 특성이며, 이를 막기 위한 **'행동 전(Pre-action) 강제 복기(Init)'** 아키텍처가 부재하면 자율성이 오히려 에러를 낳는다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 로파이 에이전트가 새로운 세션이나 작업 진입 시마다 핵심 제약 사항(`LESSONS_LEARNED.md`, 16:9 포맷, 실사 렌더링, 인물 금지 등)을 망각하고, 인터뷰를 대기하지 않은 채 내장 도구로 이미지를 무단(선제적으로) 생성하는 문제 확인.
- **세부 내용:**
  - **발견된 위반 사항 내역:**
    1. 사전 협의 및 대기 규칙 위반 (사용자 컨펌 전 독단적 실행)
    2. 가로/세로 해상도 비율 한계 및 포맷망각 (Error Case 11)
    3. 디자인 Core 3대 원칙(포토리얼리스틱, 인물 노출 절대 금지, 일렉트릭 기타 렌더링) 무시 (Error Case 12, 13, 14)
    4. 전담 폴더를 이탈한 업무 영역 침범 오류 (Scope Violation)
  - **해결 방안 (강제 Init 프로세스 도입):** 
    1. 에이전트 `SKILL.md` 최상단에 **"행동 전 반드시 `view_file` 도구로 지침(LESSONS_LEARNED.md)을 읽고 소리내어 복기하라"**는 절대 명령(System Override) 추가.
    2. 에이전트 답변 초반에 자신이 참고할 오답노트를 1문장으로 요약하게 만드는 '체크포인트(Checkpoint)' 삽입.
    3. 디자인 프롬프트 파이프라인의 핵심 템플릿(인물 없음, 실사, 기타 필수 등)을 상수로 차단(Lock-in)하여 자율도를 제한.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 문서화(`LESSONS_LEARNED.md`)를 해두더라도, LLM 모델이 자동으로 파일을 로드해서 읽을 것이란 막연한 가정이 낳은 구조적 오류 발생.
- **정책 변화 (RL Update):** 
  - 에이전트들의 지식 의존성을 맹신하지 않고, **명시적 읽기(Read) Action Step**을 필수 프로세스(System Init)로 의무 편입.
  - 박상무 봇의 해결 기획안을 수용하여, 로파이 뿐만 아니라 향후 개발될 모든 에이전트에 `강제 Initialize` 시스템 룰을 이식할 것.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/Troubleshooting]]
- **Related:** [[에이전트_권한_및_방관리_정책]], [[10_Wiki/System_Policy/Agent_Rules/Agent_Room_Management_Policy]]
- **Raw Source:** [[00_Raw/로파이-error.md]]
