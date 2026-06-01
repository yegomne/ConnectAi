---
id: 593a20e2-6d2c-4903-8d05-4c07d3b0362f
aliases: [TaskJelly 개발 로그, 태스크젤리 포스트모템, TaskJelly v1.1.1]
category: "[[10_Wiki/🛠️ Projects/TaskJelly_Development_History]]"
confidence_score: 0.95
tags: [TaskJelly, 포스트모템, 트러블슈팅, 글래스모피즘, 도파민대시보드, Tauri, Vercel, Zustand]
entities: [TECH: React, TECH: Vite, TECH: Zustand, TECH: React-Spring, TECH: Dnd-Kit, TECH: Vercel, TECH: Tauri, ORG: TaskJelly]
last_reinforced: 2026-05-01
github_commit: ""
---

# [[TaskJelly 프로젝트 개발 히스토리 (v1.0 ~ v1.1.1)]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 정적인 타이머 앱을 '살아 숨 쉬는 젤리'로 진화시킨 글래스모피즘 기반 프론트엔드 설계부터, 시각적 도파민 보상 시스템(잔디, 폭죽, 게이지) 구축 및 Vercel/Tauri 배포 파이프라인 최적화까지의 여정을 기록한 마스터 포스트모템입니다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 
  - **인지 심리학 기반 UI/UX:** 투명도와 블러(`backdrop-filter`)를 세밀하게 조정한 글래스모피즘, 그리고 `react-spring`을 통한 숨 쉬는(Breathing) 애니메이션이 사용자의 포커스 몰입감을 극대화함.
  - **상태 관리의 최적화:** `Zustand`를 활용하여 타이머(TimerStore)와 할 일(TaskStore) 상태를 분리하고, 렌더링마다 색상이 깜빡이는 플리커링 문제를 내부 해싱(Hashing) 및 순차 할당 로직으로 완벽하게 통제함.
  - **도파민 루프(보상 시스템) 자동화:** 작업 완료 시 강제 팝업 대신 백그라운드 게이지 상승과 캔버스 폭죽(Confetti) 연출을 통해 흐름을 끊지 않으면서도 즉각적인 도파민을 제공. 매일 오전 7시 자동 초기화 및 30일 잔디 그래프로 장기적 성취감(Done Storage) 설계.
  - **Lean 배포 파이프라인:** Vercel의 커스텀 도메인 매핑 오류와 Tauri 데스크톱 빌드 버전 불일치 문제를 해결하며, 버전 관리의 진실의 원천(Source of Truth)을 일원화하는 파이프라인을 확립.
- **세부 내용 요약 (핵심 마일스톤):**
  - **초기 셋업:** Vite + React + Zustand 기반 뼈대 구축 및 `@dnd-kit` 드래그 앤 드롭 정렬 도입.
  - **디버깅 & 최적화:** TS 엄격 모드 런타임 에러 해결, 모바일 스크롤 충돌 제어, 이중 스크롤바 제거.
  - **레이아웃 안정화:** 반복 업무 보관소의 시간 시각화 그래프(소프트 민트 그린), 우측 패널 듀얼 모드 위젯 정렬, 말줄임 효과(ellipsis)를 통한 텍스트 오버플로우 방어.
  - **프로덕션 배포 (v1.1.1):** .exe 보안 이슈 해결을 위한 .zip 패키징, 윈도우 트레이 백그라운드 실행 유지, Vercel DNS CNAME 매핑 완료.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 이 기록은 단순한 과거의 백업 파일이 아닙니다. 추후 대표님이 구상하실 **'주식 분석 대시보드'** 등 새로운 애플리케이션을 개발할 때, **'React-Spring 애니메이션 및 도파민 인터랙션 설계도'**이자 **'Tauri 기반 크로스 플랫폼 배포 트러블슈팅 가이드'**로 즉시 재사용할 수 있는 무적의 지식 파이프라인입니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 00_Raw 폴더의 장문 기록을 A-Wiki 구조에 맞게 핵심 패턴 위주로 재배열 및 압축함.
- **정책 변화:** 단일 프로젝트 완료 시 파편화된 로그를 '마스터 포스트모템' 하나로 통합하여 🛠️ Projects 폴더에 저장하는 RL 보상 로직 강화.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects/TaskJelly]]
- **Related:** [[도돌이표]], [[Music_Shorts_Diary_Archive]]
- **Raw Source:** [[99_Archive/Raw_Backup/[AWIKI_DONE]_TaskJelly_Development_History.md]]
