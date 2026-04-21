---
id: TASKJELLY-DEV-1.0
aliases: [TaskJelly 개발 로그, 젤리바 히스토리, 글래스모피즘 UI]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 1.0
tags: [project, taskjelly, react, zustand, glassmorphism, UI]
last_reinforced: 2026-04-21
github_commit: "pending"
---

# [[TaskJelly 프로젝트 개발 히스토리 (v1.0 Glassmorphism)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 투명한 글래스모피즘 기반의 TaskJelly 포모도로 앱의 상태 관리(Zustand)를 분리하고, 렌더링 플리커링을 차단한 반응형(React-spring) 알약 UI 1차 백업이 성공적으로 기록되었습니다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 상태와 UI가 분리된 React/Zustand 프론트엔드 아키텍처 및 글래스모피즘(Glassmorphism) 시각 최적화 패턴.
- **세부 내용:**
  1. **초기 셋업:** Vite React 보일러플레이트 제거 및 순수 포커스/백그라운드 UI 구조 확립 (`e:\TaskJelly\app`).
  2. **상태 관리 전역화:** Zustand를 활용해 `TimerStore.ts`(시간 제어 로직)와 `TaskStore.ts`(할 일 목록 제어)로 완벽히 분리.
  3. **핵심 반응형 컴포넌트 (`JellyBar`):** `react-spring`을 사용하여 유휴/포커스에 따른 호흡(Breathing) 및 클릭 시 진동(Shake) 애니메이션 매핑.
  4. **무지개 파스텔 테마 고정 알고리즘:** `Math.random()`으로 인한 리렌더링 색상 플리커링 현상 차단을 위해, 문자열 해싱(Hashing) 알고리즘과 `useMemo`로 `taskId` 기반 6가지 파스텔 컬러 영구 할당 매핑.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌 (디자인 수정):** 유리의 불투명도가 높아(Opacity Fail) 뒷배경이 비치지 않는 '플라스틱 질감' 문제가 있었습니다. 이를 `rgba(0.45 ~ 0.55)` 하향, `backdrop-filter: blur(18px) saturate(130%)` 적용, 그리고 굵은 외부 반사광 테두리(`1.5px solid rgba(255, 255, 255, 0.6)`) 적용을 통해 완벽히 극복했습니다.
- **정책 변화:** UI 컴포넌트의 컬러 매핑 시 렌더링 불일치(Flickering)를 차단하기 위해, 앞으로 모든 무작위성은 '식별자 해싱 기반 고정값' 정책을 우선으로 사용합니다. 단일 Active Color 클래스는 즉각 폐기되었습니다.

## 🔗 지식 연결 (Graph)
- **Parent:** [[TaskJelly_Project]]
- **Related:** [[Zustand_Architecture]], [[Glassmorphism_UI_Pattern]], [[React_Spring_Animation]]
- **Raw Source:** `[[00_Raw/TaskJelly_Development_History.md]]` (구조화 후 휴지통 이동)
