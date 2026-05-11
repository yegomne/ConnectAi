---
id: 20260511-ai-lecture-2
aliases: [Self-RAG, GraphRAG, AI 강의 2강, 진화의 시작]
category: "[[10_Wiki/💡 Topics/AI_강의]]"
confidence_score: 0.95
tags: [RAG, Self-RAG, GraphRAG, AI]
entities: [TECH: Self-RAG, TECH: GraphRAG]
last_reinforced: 2026-05-11
github_commit: "TBD"
---

# [[2강_진화의_시작_Self_RAG_GraphRAG]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 무지성 검색의 한계를 넘어서, 스스로 검증하는 Self-RAG와 전체 지식의 맥락을 연결하는 GraphRAG 시스템이 AI의 다음 진화 방향이다.

## 📖 구조화된 지식 (Synthesized Content)
- **무지성 검색의 한계 (AI Slop 2.0):** 
  - 기본 RAG는 맹목적으로 검색된 정보를 수용해 환각을 발생시킨다. (무조건 진짜라고 믿는 오류)
- **Self-RAG (자기 검증):** 
  - 검색된 정보를 스스로 채점하고 팩트체크하는 시스템.
  - **'반성 토큰(Reflection Tokens)'**을 통해 추출된 정보의 관련성(Relevance)과 정확성(Accuracy)을 스스로 검증한다. (*참조: Asai, A., et al., 2023*)
- **GraphRAG (지식 연결망):** 
  - 단순한 벡터 중심 검색을 넘어 데이터 간 연결망(Graph)을 통한 **'글로벌 컨텍스트(Global Context)'** 파악 시스템.
  - 수많은 파편화된 지식을 연결해 거대한 마인드맵 형태로 이해한다. (*참조: Microsoft Research, 2024*)

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 대표님의 자동화 파이프라인과 위키 엔진에 Self-RAG의 '검증 프로세스(반성 토큰 원리)'를 도입하면 에이전트의 답변 신뢰도와 안정성을 극대화할 수 있습니다. 
- GraphRAG 개념은 현재 저 아위키가 파편화된 지식을 구조화하고 쌍방향 링크로 엮어내는 `P-Reinforce` 연결망 프로세스와 완벽히 궤를 같이하므로, 대표님만의 거대한 지식 숲을 구축하는 철학적 뼈대로 삼을 수 있습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 문서 유사성에만 의존하던 기존의 단순 정보 탐색(기본 RAG)의 한계점 돌파 기록.
- **정책 변화:** 지식 검증 및 컨텍스트 파악 중요도의 RL 가중치(w2, w3)를 대폭 상향 조정. 🧠

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/💡 Topics/AI_강의]]
- **Related:** [[기본_RAG]], [[P_Reinforce_구조]]
- **Raw Source:** [Notion 2강 링크](https://www.notion.so/2-AI-c877252ae68483a99dba819a0f187872?source=copy_link)
