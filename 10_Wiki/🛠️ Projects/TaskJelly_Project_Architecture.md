---
id: taskjelly-v1-glassmorphism
aliases: [TaskJelly, 젤리바, 태스크젤리]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 0.95
tags: [TaskJelly, React, Vite, Zustand, Glassmorphism, UIUX, Productivity]
last_reinforced: 2026-04-26
github_commit: "TBD"
---

# [[TaskJelly 프로젝트 아키텍처 및 개발 히스토리]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> TaskJelly는 글래스모피즘 기반의 직관적인 타이머 및 할 일 관리 앱으로, 작업 시간에 비례하는 도파민 보상 시스템과 정교한 상태 관리로 몰입을 극대화한다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:**
  - **글래스모피즘 최적화:** 반투명도(0.45~0.55)와 강한 배경 블러(`backdrop-filter: blur(18px) saturate(130%)`), 선명한 흰색 테두리 사용이 입체감과 투과율을 동시에 높인다.
  - **플리커링 방지 (렌더링 안정화):** 동적 컬러 배정 시 `Math.random()`을 피하고, `index` 기반 순차 할당이나 `taskId` 해싱을 활용해 리렌더링 시에도 색상이 고정되도록 처리해야 한다.
  - **테마 및 색상 심리학 일치:** 신규 컴포넌트 추가 시 강제 인라인 스타일(예: 단순 화이트/블랙)이 아닌 주변 컴포넌트의 컬러 팔레트를 이식해야 가독성과 전체적인 일관성이 유지된다.
  - **도파민 보상 시스템 연동:** 단순 완료 체크를 넘어, 몰입한 시간에 비례하는 점수 보상(완료 점수 = 10점 + 설정 분 × 2점)과 파티클 효과(폭죽)를 더해 사용자의 성취감을 지속적으로 자극한다.

- **세부 내용:**
  - **핵심 기술 스택:** Vite React, Zustand(`TimerStore`, `TaskStore`), `@dnd-kit` (드래그 앤 드롭), `@react-spring/web` (애니메이션), `canvas-confetti`.
  - **주요 UI 컴포넌트:**
    - `JellyBar`: 글래스모피즘 기반의 알약 형태 할 일 바. (숨쉬는 애니메이션 및 클릭 진동 적용)
    - `DailyGauge`: 성취에 따라 차오르는 도파민 점수 바. (매일 오전 7시 초기화, 100점 달성 후 잉여 점수 이월 로직)
    - `StatsWidget`: 나의 도파민 기록장. 주간 단위(일~토) 고정 잔디 그래프 형태로 성취도 표시.
    - `RecurringWidget`: 반복 업무 보관소. 남은 시간에 따른 미니 그래프(소프트 민트 그린 톤) 시각화.
  - **주요 디버깅 및 트러블슈팅:**
    - **Dnd-kit & 클릭 이벤트 충돌 해결:** `PointerSensor`에 `activationConstraint: { distance: 5 }` 설정으로 5픽셀 이상 이동 시에만 드래그로 판정.
    - **모바일 스크롤 버그 차단:** 드래그 앤 드롭 영역에 CSS `touch-action: none;` 처리.
    - **전역 가로 스크롤 이탈 현상:** 루트 컨테이너 및 `.stats-sidebar` 패널 내부에 `overflow-x: hidden;` 적용하여 스크롤바 완전 박멸.
    - **TypeScript 런타임 에러 완전 제거:** import 분리, any 제거, 타임아웃 이벤트 타입 명시(`ReturnType<typeof setTimeout>`).

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 없음 (TaskJelly 관련 신규 지식 생성)
- **정책 변화:** 프론트엔드 UI/UX 개발에 있어 기능적 구현만큼 '시각적 테마 일관성'과 '렌더링 깜빡임 억제'가 사용자 웰빙에 직접적 영향을 미친다는 것을 깨달음. 해당 디자인 원칙을 UI 개발의 핵심 RL 가중치로 상향 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[🛠️ Projects]]
- **Related:** [[UI_UX_디자인_심리학]], [[React_상태_관리_Zustand]]
- **Raw Source:** [[00_Raw/TaskJelly_Development_History.md]], [[00_Raw/taskjellyfix.md]]
