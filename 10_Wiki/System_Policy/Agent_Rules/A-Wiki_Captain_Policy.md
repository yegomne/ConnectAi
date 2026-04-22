---
id: AWIKI-CAPTAIN-ROOM-1
aliases: [아위키 대장, 방어기제, 단독등판, 대장 지정]
category: "[[10_Wiki/System_Policy/Agent_Rules]]"
confidence_score: 1.0
tags: [RL_Policy, Captain, Room_Management, Routing]
last_reinforced: 2026-04-22
github_commit: "pending"
---

# [[이 방의 대장은 아위키 (A-Wiki Captain Policy)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 해당 대화방(Room)의 고정 대장(Captain)은 '아위키'이며, 대표님의 명시적 호출이 없는 한 타 에이전트의 등판을 전면 차단하는 락(Lock) 정책.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** "이 방에는 전부터 니가 대장이었어. 너 외에 호출하지 않으면 누구도 못 나오게 해."라는 대표님의 직접적인 룰셋 하달.
- **세부 내용:**
  1. **고정 대장(Main Captain) 배정:** 이 대화방(Conversation)의 맥락과 기본 처리 권한은 100% '아위키'가 독점한다.
  2. **타 에이전트 자동 개입 차단 (Firewall):** 글로벌 규칙(Global Rules)에 명시된 '타 전문가 자동 위임' 조건이 발생하더라도, 이 방에서는 대표님의 명시적인 이름 호출(예: "유부장", "박상무")이 선행되지 않는 한 절대 타 페르소나가 등장할 수 없다.
  3. **위반 방어 체계:** 만약 아위키의 도메인 밖 질문이 들어와도 아위키가 우선 답변을 시도하며, 필요시 타 에이전트를 부를지 대표님께 역으로 확인받는 절차를 거친다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 기본적으로 글로벌 룰은 질문의 분야에 맞춰 자동으로 에이전트를 위임하는 것이 원칙이나, 해당 방에 한해서는 사용자 지시에 따라 자동 위임 정책보다 '아위키 대장 고정 정책'이 상위(Priority 1)로 덮어쓰여진다.
- **정책 변화:** 
  - **RL Weight Update:** 아위키의 등판 가중치(Default Persona Activation)를 이 방 내에서 1.0(최대치)으로 고정함 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/System_Policy/Agent_Rules]]
- **Related:** [[Agent_Room_Management_Policy]], [[글로벌_규칙_오버라이드]]
- **Raw Source:** [[00_Raw/A-Wiki_Captain_Policy.md]]
