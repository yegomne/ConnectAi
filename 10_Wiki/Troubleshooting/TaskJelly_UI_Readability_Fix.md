---
id: a7f8e912-3b4c-4d5e-b6f7-g8h9i0j1k2l3
aliases: [TaskJelly 다크모드 병 예방, TaskJelly UI 투명인간 에러, RecurringWidget UI 가독성 패치]
category: "[[10_Wiki/Troubleshooting]]"
confidence_score: 0.95
tags: [UI_UX, Glassmorphism, CSS, Theming, Consistency]
last_reinforced: 2026-04-21
github_commit: "Pending"
---

# [[TaskJelly 위젯 가독성 및 디자인 테마 동기화 패치]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 새로운 UI 컴포넌트를 부착할 때는 단순히 독단적으로 디자인을 짜는 것이 아니라, 기존 주변 컴포넌트의 컬러 매트릭스와 디자인 시스템을 이식(Theme-Sync)해야만 UI 가독성 붕괴(투명 인간 현상)를 막을 수 있다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 이른바 '다크모드 병'. 밝은(Light) 테마 기반의 레이아웃에서 관성적으로 다크 테마용 CSS(`color: white`, `background: rgba(255,255,255,0.2)`)를 하드코딩하여 UI 요소를 시각적으로 잃어버리는 패턴 방지 가이드.
- **세부 내용:**
  - **인라인 스타일 근절:** `<span style={{color: 'white'}}>` 와 같은 1회성 인라인 색상 코드는 테마 유연성을 떨어뜨리고 가독성 에러의 주범이 되므로 CSS 클래스로 분리해야 한다.
  - **테마 통일화 (Theme Sync):** 메인/보조 폰트 컬러를 확실히 대비가 되는 `#334155`(다크 네이비), `#64748b` 등으로 교체하고, 버튼 테마는 주변 핵심 버튼(예: `TaskInput`의 파스텔 바탕 및 핑크 포인트 `#fb7185`)의 스펙을 그대로 상속받아 사용해야 튀지 않고 자연스럽다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 독립적인 컴포넌트는 알아서 잘 보이리라는 착각으로 개발했으나, 애플리케이션 전체의 밝은 글래스모피즘(backdrop-filter) 톤에서는 하얀 폰트와 반투명 배경이 합쳐져 렌더링이 소실되는 구조적 한계 발생.
- **정책 변화:** 신규 UI 컴포넌트 추가 시, 가독성 확보 전제 조건으로 기존 Color Palette와 Design System을 필수 참조하도록 유부장(개발) 스킬셋에 테마 강제 참조 룰을 주입함 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[Troubleshooting]]
- **Related:** [[Glassmorphism UI Error]], [[Design System Rules]], [[TaskJelly Work Log]]
- **Raw Source:** [[00_Raw/taskjellyfix.md]]
