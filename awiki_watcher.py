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
