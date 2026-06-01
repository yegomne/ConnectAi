---
id: 5f9e2b14-8a1a-4c8d-b033-91c2dfae83a2
aliases: [방관리, 에이전트_호출_제어, 로파이_이탈방어]
category: "[[10_Wiki/System_Policy/Agent_Rules]]"
confidence_score: 0.98
tags: [RL_Policy, Room_Management, Routing]
last_reinforced: 2026-04-21
github_commit: "Pending"
---

# [[에이전트 권한 및 방 관리(Room Management) 최적화 정책]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 프로젝트 폴더별 독점권은 프로젝트의 일관성을 보호하기 위함이며, 무분별한 에이전트 난입의 면죄부가 될 수 없다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 특정 폴더(예: `Lo-fi Moment`)에 설정된 100% 전담 룰로 인해, 관련된 렌더링 지시가 아닌 일반 질문이나 타 에이전트 지정 호출 상황에서도 전담 에이전트(로파이)가 맥락을 뚫고 튀어나오는(Hijacking) 문제 분석.
- **세부 내용:**
  - **권한 유연성 원칙:** 프로젝트 전담 에이전트는 사용자가 '명확하게 해당 에이전트의 역할과 연관된 지시'를 내렸을 때만 개입해야 한다.
  - **명시적 호출 1순위:** 대표님이 채팅창에 특정 에이전트(예: '아위키')의 이름을 직접 거론한 경우, 폴더의 독점권(Monopoly)은 잠시 무력화되며 호출받은 에이전트가 단독으로 등장할 수 있는 패스(Pass)가 주어진다.
  - **판단 레이어(Gatekeeper) 추가:** 에이전트는 작업에 개입할 때 "현재 대표님의 질문 맥락이 나의 고유 업무(예: 기타 연주, 음악 렌더링)에 부합하는가?"를 먼저 검사한 뒤 등판해야 한다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 기존 `Global Rule #5`에 삽입된 '로파이 100% 전담 보장' 문구가 너무 하드코딩된 형태로 적용되어, 예외 사항에 대한 유연한 대처가 불가능했음.
- **정책 변화 (RL Update):** 
  - 대표님의 핵심 피드백 "여기서 니가 왜 나와?"를 강력한 Negative Reward(패널티)로 적용.
  - 이를 통해 에이전트 신경망이 방 관리 권한에 대한 컨텍스트를 스위칭하도록 Policy 가중치(RL Weight)를 성공적으로 재설정함.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/System_Policy]]
- **Related:** [[1회성_명시적_호출_우선권]], [[로파이_운영_지침(LESSONS_LEARNED)]]
- **Raw Source:** 사용자(예곰) 채팅 피드백 (2026-04-21)
