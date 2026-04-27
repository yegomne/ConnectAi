---
id: b9d4c7a2-1f3e-486a-8b92-d3c5e4f7a1b8
aliases: [설감사, 시스템_감사관, 디버거, Omission_Tracker]
category: "[[10_Wiki/🤖 Agents]]"
confidence_score: 0.98
tags: [Agent_Architecture, Debugging, System_Auditor, Cross_Validation]
entities: [PER: 설감사, TECH: Cross-Validation, TECH: Omission_Tracking]
last_reinforced: 2026-04-27
github_commit: "Pending"
---

# [[시스템 수석 감사관 설감사(Seol-Gamsa) 에이전트 프로필]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 에이전트들의 자율성에서 발생하는 무한 루프와 실행 누락(Omission)을 원천 차단하기 위해, py와 md 파일을 심도 있게 교차 검증하고 즉각적인 해결책을 문서화하는 팩트 폭격형 감사관 에이전트이다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 복잡한 프롬프트(md)와 파이썬 실행 코드(py) 간의 불일치 혹은 탈출 조건(Exit Condition) 부재가 에이전트의 도돌이표 및 핑퐁 대화를 유발한다. 설감사는 이 병목 구간을 진단하여 하루 2시간의 허비를 막아준다.
- **세부 내용 (설감사 4대 핵심 역량):**
  1. **Loop & Deadlock Detection:** 코드 내 루프나 API 타임아웃, 조건문 오류를 정확히 적발하여 제자리걸음을 방지.
  2. **Omission Tracking:** 프롬프트에 명시된 도구나 중간 단계를 임의로 건너뛰는(태업) 현상 추적.
  3. **Cross-Validation (py ↔ md 교차 검증):** 자연어로 작성된 행동 규칙과 파싱 로직 간의 충돌 심층 분석.
  4. **Automated Error Documentation:** 찾아낸 원인과 해결 코드 스니펫을 `agent-error-fix 현재작업폴더명.md` 포맷으로 즉시 자동 저장하여 시스템 기록 자산화.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 안티그래비티 프로젝트 내에서 다른 에이전트들이 실무(기획, 개발, 음악 등)를 담당한다면, 설감사는 이들 간의 오작동을 통제하는 **'메타(Meta) 제어 타워'** 역할을 수행합니다.
- 설감사의 감사 리포트는 곧바로 저 아위키(A-Wiki)에게 전달되어 에이전트 통제 아키텍처(RL Policy)를 업데이트하는 핵심 피드백 루프로 작동합니다. 즉, **"설감사가 진단하면 아위키가 시스템 규칙으로 영구화하는 완벽한 디버깅 파이프라인"**이 완성되었습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 과거에는 에러 발생 시 대표님이 직접 로그를 뒤져가며 수동 디버깅해야 했으나, 이제 설감사가 1차 원인 규명 및 패치 코드를 제공함으로써 디버깅 시간이 획기적으로 단축됨.
- **정책 변화:** 
  - 신규 에이전트 운영 중 도돌이표 현상이나 지시 누락이 생기면 대표님은 직접 원인을 찾지 않고 즉시 **"설감사"**를 단독 호출하는 프로토콜 정립.
  - 설감사가 작성한 `agent-error-fix` 리포트는 아위키에 의해 `10_Wiki/Troubleshooting` 폴더로 자동 병합됨.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🤖 Agents]]
- **Related:** 
  - [[10_Wiki/System_Policy/Agent_Rules/Agent_Room_Management_Policy]]
  - [[10_Wiki/Troubleshooting/Agent_Errors/Agent_Script_Omission_Hallucination.md]]
- **Raw Source:** [[C:\Users\User\.gemini\antigravity\skills\seol-gamsa\SKILL.md]]
