---
id: MOC-PROJECTS
aliases: [Projects Dashboard, 프로젝트 모아보기, 🛠️ Projects]
tags: [MOC, dashboard, projects]
---

# 🛠️ Projects Dashboard (관제탑)

이 문서는 `🛠️ Projects` 폴더 내에서 생성되는 모든 프로젝트 관련 지식, 개발 로그, 히스토리를 한곳에서 내려다볼 수 있는 **지식 관제탑(MOC: Map of Content)**입니다.
앞으로는 문서의 속성(Frontmatter)에서 `category: "[[10_Wiki/🛠️ Projects]]"`라고 링킹하면, 어지럽게 더미 파일이 생기는 것이 아니라 **바로 이곳, '지식의 허브'로 모든 선이 연결**됩니다.

## 📌 전체 프로젝트 목록
- [[TaskJelly_Development_History]] : TaskJelly (v1.0 Glassmorphism) 시스템 구조화 및 도파민 보상망 설계 기록

---

### 🔮 Dataview 자동화 보드
*(※ 옵시디언 커뮤니티 플러그인 `Dataview`가 설치되어 있다면, 아래 표에 프로젝트들이 자동으로 업데이트됩니다!)*

```dataview
table last_reinforced as "마지막 강화일", confidence_score as "신뢰도 점수"
from "10_Wiki/🛠️ Projects"
sort last_reinforced desc
```
