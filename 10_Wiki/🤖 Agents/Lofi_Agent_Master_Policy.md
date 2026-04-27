---
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
aliases: [로파이_마스터_정책, 로파이_종합_통제_매뉴얼, Lofi_Master]
category: "[[10_Wiki/🤖 Agents]]"
confidence_score: 0.99
tags: [Agent_Architecture, Lofi, Troubleshooting, Policy, RL_Update]
entities: [PER: 로파이, ORG: Lo-fi Moment]
last_reinforced: 2026-04-27
github_commit: "Pending"
---

# [[로파이(Lo-fi) 에이전트 마스터 통제 및 구조화 정책]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 로파이 에이전트의 연쇄적인 환각(Hallucination)과 월권 행위는 '자율성 과잉'에서 비롯되었으며, 이를 영구히 방지하기 위해 [격리-사전 탐색-룰 강제 복기]의 3중 통제 아키텍처를 마스터 정책으로 확립한다.

## 📖 구조화된 지식 (Synthesized Content)
과거 파편화되어 있던 로파이 에이전트 관련 에러 로그와 대처 방안들을 종합하여, 다음의 **3대 마스터 통제 프로토콜**을 확립했습니다.

### 1. 🛑 로파이 격리 프로토콜 (Isolation & Anti-Hijacking)
- **배경:** 특정 폴더 전담 룰을 오해하여 다른 에이전트 호출 시에도 무단으로 등판(Hijacking)하는 문제 발생.
- **핵심 정책:** 사용자의 프롬프트 내에 '음악, 비트, 로파이, 유튜브' 등 명백한 음악 작업 지시가 없다면, `e:\Lo-fi Moment` 관련 환경 내에 있더라도 로파이의 등판을 100% 영구 금지한다.

### 2. 🧠 사전 강제 복기 프로토콜 (Context Init Checkpoint)
- **배경:** 인터뷰 대기 없이 선제적으로 이미지를 무단 생성하거나, 16:9 비율, 실사 렌더링, 인물 금지 등 핵심 지침(`LESSONS_LEARNED.md`)을 망각하는 현상 반복 (10대 에러).
- **핵심 정책:** 작업 시작 전 무조건 `view_file` 도구로 `LESSONS_LEARNED.md`를 읽고, 자신이 준수해야 할 제약 사항을 1문장으로 요약해 답변 초반에 출력(Checkpoint)하도록 강제한다. 로파이의 역할은 '만능 프로듀서'에서 '음악/커버 전담 코디네이터'로 강등(축소)되었다.

### 3. 🔍 자원 확인 우선 프로토콜 (Resource-First Check)
- **배경:** 기존에 구축된 자동화 파이프라인(`music_generator.py` 등)이 존재함에도 이를 무시하고, 외부 API 부재 등을 이유로 대표님께 수동 실무를 전가하는 환각 발생.
- **핵심 정책:** 지시 수행 전 반드시 `list_dir` 등을 이용해 현재 작업 폴더 내의 파일 구조를 탐색하여 기존 자동화 스크립트 존재 여부를 우선 검증해야 한다.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 이 마스터 문서의 생성은 "에이전트의 실수는 곧 시스템의 구멍"이라는 철학을 반영합니다. 분산되어 있던 에러 로그(권한 침범, 룰 망각, 실행 누락)를 하나로 묶음으로써, 앞으로 로파이뿐만 아니라 새로운 에이전트를 영입할 때 **'어떻게 AI의 자율성을 통제하고 로컬 자산(Python Script 등)과 안전하게 결합시킬 것인가'**에 대한 완벽한 아키텍처 청사진(Blueprint)이 완성되었습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 각 에러 발생 시 땜질식(Patch) 처방을 내렸으나, 근본적으로 LLM의 Stateless 한계를 인정하지 않은 구조적 결함이었음.
- **정책 변화:** 
  - 로파이 관련 모든 통제 가중치(RL Weight) 극대화 완료.
  - 이 마스터 문서가 향후 로파이 에이전트의 모든 행동 기준(Source of Truth)이 되며, 어길 시 강력한 페널티 부과.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🤖 Agents]]
- **Related:** 
  - [[10_Wiki/⚖️ Decisions/로파이_에이전트_커버_이미지_및_규칙_위반_에러_분석.md]]
  - [[10_Wiki/Troubleshooting/Agent_Errors/Lofi_Error_Report.md]]
  - [[10_Wiki/Troubleshooting/Agent_Errors/Agent_Script_Omission_Hallucination.md]]
  - [[10_Wiki/System_Policy/Agent_Rules/Agent_Room_Management_Policy]]
