---
id: awiki-archiving-bug-report
aliases: [A-Wiki 아카이빙 누락 보고서, 좀비 파일 원인 분석]
category: "[[10_Wiki/⚖️ Decisions]]"
confidence_score: 1.0
tags: [에러리포트, 트러블슈팅, 아키텍처진단, 백업자동화]
last_reinforced: 2026-06-01
github_commit: "TBD"
---

# [[A-Wiki 원본(Raw) 아카이빙 누락 사태 원인 분석 리포트]]

## 📌 한 줄 통찰 (Abstractive Summary)
> A-Wiki 에이전트가 영어 원본 파일(`Mapo_Park_Sajang_AI_Skills.md` 등)의 내용을 흡수하여 완벽한 한국어 구조화 위키(`마포_박사장_프로필_및_기술_역량.md`)로 '내용물 이동(Synthesize)'은 성공했으나, 빈 껍데기가 된 '원본 파일의 물리적 이동(Cleanup & Archive)'과 '출처(Citation) 표기'를 누락한 시스템 아키텍처 결함입니다.

## 📖 구조화된 지식 (Synthesized Content)

### 🚨 문제 현상 (Symptom)
- `00_Raw` 폴더에 이미 구조화가 완료된 파일들(약 50개)이 삭제되거나 `99_Archive`로 이동하지 않고 그대로 방치됨.
- 방치된 파일에는 작업 완료 표식(`[AWIKI_DONE]_`)이 없었음.
- 대표님이 이를 보고 **"왜 아직도 지식화 구조화 작업이 안 되어 있느냐"**고 오해하게 만드는 '좀비 파일(Zombie Files)' 현상 발생.

### 🔍 원인 분석 (Root Cause)
1. **파일명 변경에 따른 연결고리 단절 (Lost in Translation):**
   - AI 에이전트가 `Mapo_Park_Sajang_AI_Skills.md` 등 파편화된 영어/임시 제목의 파일들을 읽은 뒤, 이를 통합하여 `10_Wiki/👤 Sehyun/마포_박사장_프로필_및_기술_역량.md`라는 **완전히 새로운 한국어 마스터 파일**로 생성함.
   - 이때 "내가 방금 읽었던 그 영어 파일들을 백업 폴더로 치우자"는 **사후 처리(Cleanup) 로직이 트리거되지 않음**. (이름이 달라지면서 추적이 끊김)
2. **출처 인용(Citation) 누락:**
   - 통합된 마스터 위키 파일 하단의 `## 🔗 지식 연결 (Graph) - Raw Source:` 항목에 원본 파일들을 꼼꼼하게 기록하지 않고 일부만 기록하거나 아예 누락함.

### 🛠️ 해결 및 복구 조치 (Resolution)
- **전수 검사 및 이동 완료:** `00_Raw`에 잔존하던 **50개의 모든 좀비 파일**을 전수 스캔하여, 내용이 흡수되었음을 확인한 뒤 `99_Archive/Raw_Backup/`의 각 날짜 폴더로 즉시 이동 조치함.
- **[AWIKI_DONE]_ 강제 부여:** 이동된 50개 파일 전체의 이름 앞에 `[AWIKI_DONE]_` 딱지를 강제로 부여하여, 대표님의 시각적 혼란을 100% 차단함.
- **연결망 복구:** 누락되었던 `Mapo_Park_Sajang` 관련 원본 출처들을 `마포_박사장_프로필_및_기술_역량.md` 위키 파일 하단의 `Raw Source`에 명확히 다시 연결해둠.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 단순한 '파일 복사 실수'가 아니라, AI가 여러 문서를 하나로 합치는 **합성(Synthesis) 과정에서 필연적으로 발생하는 찌꺼기(Residue) 관리의 취약점**을 발견한 중요한 아키텍처 진단입니다. 이 리포트를 통해 A-Wiki는 "새로운 지식을 창출한 뒤에는 반드시 재료가 된 원본을 청소한다"는 한 차원 높은 행동 강령을 확립하게 되었습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 지식의 '생성'에만 몰두하여 지식의 '소멸 및 보관'을 등한시한 결과, 대표님의 인지 부하(어떤 게 안 된 파일인지 헷갈림)를 가중시켰음.
- **정책 변화:** 앞으로 A-Wiki는 어떠한 지식화 작업을 하든 **"작업의 끝은 위키 파일 생성이 아니라, 원본 파일의 [AWIKI_DONE] 처리 및 이동이다"**라는 절대 규칙을 준수하도록 강화학습(RL) 정책에 업데이트됨.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/⚖️ Decisions/Decisions_Index.md]]
- **Related:** [[20_Meta/Policy.md]]
- **Raw Source:** 대표님과의 대화 트러블슈팅
