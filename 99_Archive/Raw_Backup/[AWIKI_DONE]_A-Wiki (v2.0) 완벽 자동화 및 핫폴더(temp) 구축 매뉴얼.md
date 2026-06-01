---
id: awiki-v2-full-automation-manual
aliases: [아위키 v2.0 자동화 통합 세팅 가이드, 핫폴더 구축 백서]
category: "[[20_Meta/Agent_Manuals]]"
tags: [P-Reinforce, Antigravity, A-Wiki, 자동화, 파이썬, 핫폴더]
last_updated: 2026-05-27
---

# 🚀 A-Wiki (v2.0) 완벽 자동화 및 핫폴더(temp) 구축 매뉴얼

## 📌 한 줄 통찰
> 단순한 지식 저장소를 넘어, 특정 폴더(`temp`)에 파일을 던지는 즉시 메인 컴퓨터가 이를 감지하고 세컨 컴퓨터의 서버를 가동해 지식을 쪼개며, 깃허브 무결성까지 완벽하게 지켜내는 완전 자율형 지식 파이프라인을 완성했다.

---

## 1. 📂 볼트 폴더 구조 및 Git 역할 분담

아위키가 에러 없이 완벽하게 구동되기 위한 최상단(`D:\Connect_Ai\`) 폴더 구조 및 권한 설정.

- **`00_Raw/`** : 보존이 필요한 공식 원시 데이터 수집용
- **`10_Wiki/`** : 아위키가 정제하고 쪼개놓은(Atomic Split) 지식 결과물이 저장되는 메인 공간
- **`temp/`** : **[신규]** 자유롭게 파일을 던져놓는 일회성 임시 핫폴더 (작업 후 찌꺼기 삭제 구역)
- **`99_Archive\Raw_Backup\`** : **[신규]** 처리가 끝난 원본 파일이 자동 보관되는 백업소

### 🛡️ Git 무결성을 위한 핵심 설정 (`.gitignore`)
볼트 최상단의 `.gitignore` 파일에 아래 내용을 반영하여 시스템 간 역할을 명확히 분리한다.
- `temp/` : (추가 필수) 지저분한 임시 작업 흔적을 깃허브에 남기지 않기 위해 Git 추적에서 배제함.
- `99_Archive/` : (추가 금지) 원본의 '영구 클라우드 백업'이 목적이므로 Git이 정상적으로 추적해야 함.

---

## 2. 🧠 아위키 에이전트 지침 업데이트 (`skill.md`)

에이전트가 `temp` 폴더의 원본을 삭제하지 않고 안전하게 보관하되, 보관소의 내용은 RAG나 리팩토링 시 절대 건드리지 않도록 '격리 구역'으로 설정한다.

**[적용 위치: `🎯 Core Mission` 6번 항목 신설]**
> 6. **원본 자동 보관(Auto-Archiving):** 임시 작업장인 `temp/` 폴더에서 원자적 분해(Atomic Split) 및 지식화 작업이 완료된 원본 문서는 절대 삭제하지 말고, 즉시 `99_Archive/Raw_Backup/` 폴더로 이동시켜라. 단, `99_Archive/` 폴더는 영구 보존용 '격리 구역(Blacklist)'이므로, 이후 수행되는 모든 RAG 검색, 문맥 분석, 지식 병합 및 리팩토링 대상에서 완벽하게 제외하여 원본 데이터의 훼손 및 검색 결과의 중복 오염을 원천 차단하라.

*(※ 아위키의 작동 방식: `temp` 폴더는 즉각 처리하는 기본 모드이며, 특정 과거 문서를 재작업하고 싶을 때는 채팅창에 경로를 짚어주면 수동 타겟팅으로 그곳으로 이동해 즉시 작업함)*

---

## 3. ⚙️ 실시간 감지 자동화 스크립트 (Python Watchdog)

아위키에게 '눈과 귀'를 달아주어, `temp` 폴더에 파일이 들어오는 즉시(딜레이 0초) Antigravity CLI를 통해 백그라운드에서 연산을 지시하는 파이썬 스크립트.

### ⚠️ 주의사항
- `temp` 폴더 청소 시 실수로 지워지는 것을 방지하기 위해, 스크립트 파일은 반드시 `temp` 바깥인 **`D:\Connect_Ai\awiki_watcher.py`** 에 저장할 것.

**[awiki_watcher.py 코드]**
```python
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 모니터링할 temp 폴더의 절대 경로
WATCH_DIR = r"D:\Connect_Ai\temp"

class AWikiTrigger(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"👀 새 문서 감지됨: {event.src_path}")
            print("🚀 아위키(A-Wiki) NLP 파이프라인 자동 호출 중...")
            # Antigravity CLI 호출 (작업 지시)
            os.system('antigravity run A-Wiki --prompt "temp 폴더에 새 파일이 감지되었습니다. 작업해."')

if __name__ == "__main__":
    event_handler = AWikiTrigger()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"🛡️ 아위키 핫 폴더 모니터링 시작: {WATCH_DIR}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()