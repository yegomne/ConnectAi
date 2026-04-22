---
id: TASKJELLY-DEV-HISTORY-1.0
aliases: [TaskJelly 개발 히스토리, TaskJelly Glassmorphism, 젤리바 컴포넌트, 포모도로 상태관리]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 1.0
tags: [project, taskjelly, react, zustand, glassmorphism, dnd-kit, typescript, troubleshooting]
last_reinforced: 2026-04-22
github_commit: "3c9aea9"
---

# [[TaskJelly 개발 히스토리 (v1.0 Glassmorphism)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> Vite+React 기반으로 Zustand 상태 관리, Glassmorphism UI, react-spring 애니메이션, 그리고 dnd-kit을 통합하여 시각적 타격감과 직관성을 극대화한 TaskJelly 프로젝트의 A to Z 구축 기록.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 상태와 UI의 분리(Zustand), 렌더링 최적화(Index 기반 해싱), 물리 기반 UX(dnd-kit 충돌 제어), 도파민 기반 보상 피드백(Daily Gauge), StatsWidget 고정 주간 뷰 UX 개선, 헤더 버튼 사이드바 통합.
- **세부 내용:**
  1. **초기 셋업 및 코어 로직:** Vite React 환경에서 `TimerStore.ts`(포모도로 코어)와 `TaskStore.ts`(할일 관리)로 분리된 Zustand 스토어 아키텍처.
  2. **핵심 UI (JellyBar):** 글래스모피즘 기반 입체 알약 형태 구현 (`rgba` 0.45~0.55, `backdrop-filter: blur(18px) saturate(130%)`). 
  3. **인터랙션 및 UX 최적화:** 
     - `@dnd-kit/core`로 드래그 앤 드롭 구현, `PointerSensor` `distance: 5`로 일반 클릭과 드래그 충돌 방지. 모바일 대응 `touch-action: none`.
     - `index` 기반 순차 할당 해싱으로 알약 바 색상의 '플리커링' 및 중복 렌더링 방지.
  4. **성취 보상 시스템 (Dopamine UX):** Task 완료 시 점수 누적, `@react-spring/web` 애니메이션 및 `canvas-confetti` 폭죽 파티클 발동.
  5. **타입 안정성 (TypeScript):** Strict Mode 런타임 에러(`any` 타입, 모듈 import 충돌 등) 전면 디버깅 및 `import type` 적용으로 빌드 에러율 0% 달성.
  6. **데이터 시각화 (StatsWidget):** 잔디 그래프를 롤링 방식에서 '이번 주(일-토)' 고정 보기로 변경하고 미래 날짜의 투명도(opacity: 0.4)를 낮춰 직관성 개선. 테마 일관성을 위한 폰트 및 중앙 정렬 레이아웃 고도화.
  7. **레이아웃 및 접근성 개선:** `App.tsx` 최상단에 있던 액션 버튼('기억 창고', '퇴근')을 `StatsWidget.tsx` 하단으로 이동 및 Column 정렬하여 사이드바로 기능(통계/히스토리)을 통합하고 상단 헤더 여백 확보.
  8. **도파민 게이지 자동화 및 잉여 점수 처리:** `lastGaugeReset` 상태를 도입하여 매일 오전 7시에 게이지를 자동 리셋하고, 100점 초과 시 보상 지급 후 잉여 점수만 렌더링되도록 `dailyGauge % 100` 연산 적용 및 persist 미들웨어에 연동.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 초기 불투명도를 너무 높게 잡아 유리의 투과성이 죽는 문제, 랜덤 배정으로 인한 리렌더링 플리커링 등 시각적 피로도 유발 이슈 발견.
- **정책 변화:** 
  1. **Glassmorphism 표준값 도출:** 굴절/반사를 위한 배경 불투명도(0.45~0.55), 블러(18px), 채도(130%), 테두리(1.5px solid rgba(255,255,255,0.6)) 공식화 🧠.
  2. **렌더링 의존성 분리:** 컴포넌트 렌더링 주기와 동적 속성(Color)을 분리하기 위해 철저한 `index` 또는 `hash` 기반의 고정 배정 알고리즘을 UI 표준으로 채택 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[TaskJelly_Project]]
- **Related:** [[Zustand_State_Management]], [[Glassmorphism_UI_Design]], [[Drag_and_Drop_UX]]
- **Raw Source:** `[[00_Raw/TaskJelly_Development_History.md]]`
