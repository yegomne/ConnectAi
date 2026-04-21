---
id: bac666d8-ab9d-4e8e-8175-3e7d68ba63a7
aliases: [MatterJelly 오류 결산, 투명 젤리바 물리 에러]
category: "[[10_Wiki/⚖️ Decisions]]"
confidence_score: 0.95
tags: [MatterJS, SVG, Glassmorphism, Physics_Engine, Troubleshooting]
last_reinforced: 2026-04-21
github_commit: "Pending"
---

# [[MatterJelly 물리 젤리바 제작 실패 및 회고]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 과도한 SVG 유리 효과와 뷰박스 좌표계 불일치는 물리 엔진 렌더링에 치명적이며, 강력한 Constraint(앵커, 슈퍼 크로스) 구조가 없으면 젤리가 형태를 유지하지 못하고 주저앉는다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** Matter.js + SVG 애니메이션을 결합한 컴포넌트(물리UI)에서 흔히 발생하는 해상도 및 장력 문제 트러블슈팅 패턴.
- **세부 내용:**
  - **크기 불일치:** `viewBox`의 설정(가상 해상도)과 Matter.js 물리 좌표계(단위)가 다를 경우 비율이 무너짐. 단일 해상도 환경으로 통일해야 함.
  - **표면 장력 상실 (Deflation):** 물리 젤리가 형태를 잡지 못하고 주저앉을 땐, 중앙 앵커(Anchor)와 마주 보는 반대편 입자들을 이어주는 '슈퍼 크로스 링크(stiffness: 0.1 등)'로 내부 압력 지지대를 뼈대처럼 세워야 함.
  - **과도한 글래스모피즘 오버 엔지니어링:** SVG 내부를 clipPath, foreignObject 등 불필요한 DOM 객체로 렌더링할 시 에러가 잦으므로, 부모 컨테이너에 단순 CSS `backdrop-filter: blur()` 처리를 하고 내부는 단순 `fill` 반투명 처리로 경량화해야 함.
  - **텍스트 오버레이 정렬:** 투명 SVG 배경 내에서 z-index 이슈 발생을 방지하기 위해 컨테이너의 뒤 배경 렌더링 요소를 비우고 중심점 위에 절대배치(absolute) 시킨 순수 텍스트 계층을 고정하는 것이 안전함.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 화려한 CSS 기법(글래스모피즘 등)을 SVG에 무리하게 적용하려 했으나, 성능과 물리 엔진의 충돌로 인해 단순화(Lean Architecture) 접근으로 회귀.
- **정책 변화:** 10_Wiki/⚖️ Decisions 에 새로운 UI 물리 엔진 개발 과정의 실패를 지식화하여, 추후 인터랙티브 웹 UI 기획 시 오버 엔지니어링 억제 가중치 상승 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[의사결정 및 실패 기록]]
- **Related:** [[MatterJS Constraints]], [[SVG Glassmorphism Optimization]], [[TaskJelly_Development_History]]
- **Raw Source:** [[00_Raw/Jelly_Error_Log.md]]
