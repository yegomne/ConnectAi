---
id: TASKJELLY-DEV-HISTORY-1.0
aliases: [TaskJelly 개발 히스토리, TaskJelly Glassmorphism, 젤리바 컴포넌트, 포모도로 상태관리]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 1.0
tags: [project, taskjelly, react, zustand, glassmorphism, dnd-kit, typescript, troubleshooting, hexagonal-architecture, automation, ui-ux, deployment]
last_reinforced: 2026-05-01
github_commit: "Pending"
---

# [[TaskJelly 개발 히스토리 (v1.0 Glassmorphism)]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 기존의 Hexagonal 아키텍처와 Glassmorphism UI 기반 위에, 상용화를 위한 도메인 연동(Vercel, Hosting.kr), 윈도우 백그라운드 트레이 지원, 듀얼 모드 위젯 및 잔디 그래프 레이아웃 최적화, 다운로드 방식(.zip) 개선 등 배포 및 사용자 경험(UX) 디테일을 완벽히 통합한 전체 개발 기록.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 상태와 UI의 분리(Zustand), 데이터 접근 계층 추상화(포트 앤 어댑터), 백그라운드 자동화(Midnight Observer, Window Tray), 시각적 피드백(Pulse Badge, Confetti), 렌더링 최적화(Index 기반 해싱), 물리 기반 UX(dnd-kit 충돌 제어), 도파민 기반 보상 피드백(비례 보상 및 잔디 그래프 실제 연동), UI 테마 통일성(명도 대비), 안정적인 배포(Vercel DNS, ZIP 패키징).
- **세부 내용 (기존 아키텍처 및 핵심 로직):**
  1. **초기 셋업 및 코어 로직:** Vite React 환경에서 `TimerStore.ts`(포모도로 코어)와 `TaskStore.ts`(할일 관리)로 분리된 Zustand 스토어 아키텍처.
  2. **핵심 UI (JellyBar):** 글래스모피즘 기반 입체 알약 형태 구현 (`rgba` 0.45~0.55, `backdrop-filter: blur(18px) saturate(130%)`). index 기반 순차 할당 해싱으로 플리커링 방지.
  3. **인터랙션 및 성취 보상:** `@dnd-kit/core`로 드래그 앤 드롭 구현, 포인터 클릭 충돌 제어. Task 완료 시 도파민 게이지 점수 누적, 폭죽 파티클 발동 및 비례 보상 시스템. 100점 초과 시 잉여 점수 렌더링 최적화.
  4. **스토리지 포트 및 어댑터 리팩토링 (Hexagonal):** 기존 Zustand `persist`를 제거하고 `IAppRepository` 포트 정의 및 `TauriAppRepository` 어댑터 구현으로 도메인 로직 보호.
  5. **반복 업무 자동화 (Midnight Observer):** 매일 오전 7시 도파민 게이지 리셋 및 반복 태스크의 백그라운드 미완료 뱃지 동기화 로직.
- **세부 내용 (신규 배포 및 UI/UX 고도화):**
  6. **대시보드 데이터 연동 및 레이아웃:** 도파민 잔디 그래프를 더미 데이터에서 실제 `dopamineHistory` 연동으로 변경하고 '오늘 심은 잔디 수' 추가. 우측 패널의 레이아웃을 Column으로 복구하여 시각적 밸런스 회복.
  7. **시인성 및 안정성 강화:** Task Input 및 새마음 리셋 버튼의 글자 짤림 방지, 텍스트 넘침에 대한 ellipsis 처리. 다운로드 시 Mac OS 버튼 비활성화로 사용자 혼동 방지.
  8. **배포 인프라 및 트레이 실행:** Vercel 프로덕션 배포 후 `taskjelly.yegomnne.com` (Hosting.kr) DNS 연결 완료. `.exe` 보안 경고 해결을 위해 `.zip` 포맷으로 다운로드 제공. 프로그램 종료 시 우측 상단 X 클릭 후에도 윈도우 시스템 트레이(Tray)에서 백그라운드 실행을 유지하여 작업 연속성 확보.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- **개발부터 배포까지의 End-to-End 파이프라인:** 이 기록은 단순한 컴포넌트 개발기를 넘어, 로컬 앱(Tauri) 상태 관리의 Hexagonal 패턴 적용과 상용 배포(Vercel, 도메인), 윈도우 네이티브 트레이 기능까지 하나의 프로덕트가 완성되는 전체 사이클을 보여줍니다. 추후 다른 SaaS 프로젝트 생성 시, 본 문서의 스토리지 어댑터 구조와 Vercel-Hosting.kr 배포 파이프라인을 템플릿으로 재사용할 수 있습니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 
  1. 기존 우측 패널 가로 배열 시도 -> 디자인 불균형 발생 -> 원래의 세로 형태로 원상복구(레이아웃 롤백).
  2. `.exe` 다이렉트 다운로드 -> 크롬 보안 이슈 발생 -> `.zip` 패키징으로 변경.
- **정책 변화:** 
  1. **배포 포맷 표준화:** 모든 설치 파일 배포 시에는 브라우저 보안 필터링 우회를 위해 `.zip` 패키징을 기본 정책으로 채택 🧠.
  2. **백그라운드 UX 정책:** 작업 관리 도구 특성상 X 버튼 클릭 시 완전 종료가 아닌 시스템 트레이 숨김을 디폴트 액션으로 정의 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[TaskJelly_Project]]
- **Related:** [[Zustand_State_Management]], [[Glassmorphism_UI_Design]], [[Drag_and_Drop_UX]], [[Tauri_Hexagonal_Architecture]], [[Vercel_Deployment_Guide]]
- **Raw Source:** `[[00_Raw/TaskJelly_Development_History.md]]`
