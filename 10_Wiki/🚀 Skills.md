---
id: MOC-SKILLS
aliases: [Skills Dashboard, 스킬 모아보기, 🚀 Skills]
tags: [MOC, dashboard, skills]
---

# 🚀 Skills Dashboard (관제탑)

이 문서는 AI 프롬프트, 도메인 연결 규칙, 배포 파이프라인 등 팀의 강력한 기술(Skill) 문서들을 응집시키는 **스킬 관제탑(MOC: Map of Content)**입니다. 
분산되어 있던 개별 스킬 마크다운 파일들이 이제 이 허브 문서를 중심축 삼아 별자리처럼 연결됩니다.

## 📌 보유 스킬 카탈로그
- *(여기에 [[스킬 문서 이름]] 형태로 직접 링크를 추가할 수 있습니다)*

---

### 🔮 Dataview 자동화 보드
*(새로운 스킬 지식이 `10_Wiki/🚀 Skills` 폴더에 생성될 때마다 아래 표에 스스로 업데이트됩니다)*

```dataview
table file.mtime as "마지막 수정일"
from "10_Wiki/🚀 Skills"
sort file.mtime desc
```
