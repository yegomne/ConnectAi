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
> 컴포넌트(글래스모피즘, D&D) 고도화, 안정성 획득(TypeScript Strict)과 더불어, 폭죽 모션 기반의 즉각적 도파민 보상망(Daily Gauge)을 적용한 TaskJelly 아키텍처 기록.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 상태와 UI가 분리된 React/Zustand 프론트엔드 아키텍처, 물리 기반 UI 확장성(D&D), 글래스모피즘 시각 최적화 및 TypeScript 엄밀성 확보 패턴.
- **세부 내용:**
  1. **초기 셋업:** Vite React 보일러플레이트 제거 및 순수 포커스/백그라운드 UI 구조 확립 (`e:\TaskJelly\app`).
  2. **상태 관리 전역화:** Zustand를 활용해 `TimerStore.ts`(시간 제어 로직)와 `TaskStore.ts`(할 일 목록 제어)로 완벽히 분리.
  3. **핵심 반응형 컴포넌트 (`JellyBar`):** `react-spring`을 사용하여 유휴/포커스에 따른 호흡(Breathing) 및 클릭 시 진동(Shake) 애니메이션 매핑.
  4. **무지개 파스텔 테마 고정 알고리즘:** `Math.random()`으로 인한 리렌더링 색상 플리커링 현상 차단을 위해, 문자열 해싱(Hashing) 알고리즘과 `useMemo`로 `taskId` 기반 6가지 파스텔 컬러 영구 할당 매핑.
  5. **물리적 드래그 앤 드롭 (D&D):** `@dnd-kit/core` 적용. `PointerSensor`의 `activationConstraint: { distance: 5 }` 옵션 설정으로 타이머 켤 때의 클릭(Touch) 이벤트 충돌을 우아하게 우회하고, CSS `touch-action: none;`으로 모바일 스와이프 시 뷰포트가 스크롤되는 불쾌한 버그 완벽 통제.
  6. **TypeScript 런타임 보호:** 타임아웃 이벤트 타입 지정(`ReturnType<typeof setTimeout>`), `import type` 분리 적용 및 모든 암묵적 `any` 변수 제거 등 엄격 룰셋(Strict Type) 준수를 통해 빈 화면(White Screen) 및 빌드 에러 원천 해결 (에러 잔존율 0%).
  7. **도파민 성취 보상 시스템 (`DailyGauge.tsx`):** Task 완료(`TimerStore`의 `finish`) 시 상태를 `memory`로 갱신하여 메인 뷰에서 분리시키고, `@react-spring/web`과 `canvas-confetti`를 결합해 게이지 카운팅 및 화면 하단의 5색 파스텔 톤 폭죽이 터지는 즉각적인 시각적 쾌감을 제공.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌 (디자인 수정):** 유리의 불투명도가 높아(Opacity Fail) 뒷배경이 비치지 않는 '플라스틱 질감' 문제가 있었습니다. 이를 `rgba(0.45 ~ 0.55)` 하향, `backdrop-filter: blur(18px) saturate(130%)` 적용, 그리고 굵은 외부 반사광 테두리(`1.5px solid rgba(255, 255, 255, 0.6)`) 적용을 통해 완벽히 극복했습니다.
- **정책 변화:** 
  1. **UI 렌더링 안정성:** 컬러 매핑 시 렌더링 불일치(Flickering) 차단을 위해 '식별자 해싱 기반 고정값'을 우선 사용. 단일 색상(Active) 부여 방식 전면 폐쇄.
  2. **인터랙션(UX)의 충돌 처리:** 드래그 컴포넌트(D&D) 안에서 클릭 이벤트(타이머 실행 등)가 발생할 경우, 드래그 활성화에 최소 이동 거리(`distance`) 제약을 두어 터치와 스와이프를 분리.
  3. **타입 안전성 (Type Safety):** 런타임 버그 방지를 위해 동적 변수에 `any` 사용을 금지하며 명시된 TypeScript 시그니처만 사용함을 지식 베이스에 각인 🧠.
  4. **도파민 주도 UX (Dopamine-Driven Experience):** 아무리 작은 Task라도 수행 완료 시 즉각적이고 강렬한 시각적 피드백(폭죽, 게이지)을 제공하여 사용자의 다음 행동을 유도하는 보상 회로 패턴을 UI/UX 핵심 정책으로 채택함.

## 🔗 지식 연결 (Graph)
- **Parent:** [[TaskJelly_Project]]
- **Related:** [[Zustand_Architecture]], [[Glassmorphism_UI_Pattern]], [[React_Spring_Animation]]
- **Raw Source:** `[[00_Raw/TaskJelly_Development_History.md]]` (단일 진실의 원천 - 불변 보존)
