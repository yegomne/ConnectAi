import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import docx
except ImportError:
    docx = None

# 경로 설정
WATCH_DIR = r"D:\Connect_Ai\temp"
ARCHIVE_DIR = r"D:\Connect_Ai\99_Archive\Raw_Backup"

os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

class AWikiTrigger(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
            
        src_path = Path(event.src_path)
        ext = src_path.suffix.lower()
        
        # 임시 파일 무시 (엑셀 열 때 생성되는 ~$ 파일 등)
        if src_path.name.startswith("~"):
            return
            
        if ext == '.md':
            # Markdown 파일: 기본 A-Wiki 처리 로직
            print(f"👀 새 마크다운 감지됨: {src_path}")
            print("🚀 아위키(A-Wiki) NLP 파이프라인 자동 호출 중...")
            os.system('antigravity run A-Wiki --prompt "temp 폴더에 새 파일이 감지되었습니다. 작업해."')
            
        elif ext in ['.xlsx', '.xls']:
            print(f"👀 새 엑셀 감지됨: {src_path}")
            self.parse_excel_to_md(src_path)
            
        elif ext == '.docx':
            print(f"👀 새 워드 감지됨: {src_path}")
            self.parse_word_to_md(src_path)
            
    def parse_excel_to_md(self, filepath):
        if pd is None:
            print("❌ pandas 라이브러리가 없어 엑셀을 처리할 수 없습니다.")
            return
            
        try:
            # 모든 시트를 읽어서 마크다운으로 변환
            sheets = pd.read_excel(filepath, sheet_name=None)
            md_content = f"# 엑셀 자동 파싱 결과: {filepath.name}\n\n"
            
            for sheet_name, df in sheets.items():
                md_content += f"## Sheet: {sheet_name}\n"
                md_content += df.to_markdown(index=False)
                md_content += "\n\n"
                
            self._save_md_and_archive(filepath, md_content)
        except Exception as e:
            print(f"❌ 엑셀 파싱 중 에러 발생: {e}")
            
    def parse_word_to_md(self, filepath):
        if docx is None:
            print("❌ python-docx 라이브러리가 없어 워드를 처리할 수 없습니다.")
            return
            
        try:
            doc = docx.Document(filepath)
            md_content = f"# 워드 자동 파싱 결과: {filepath.name}\n\n"
            
            for para in doc.paragraphs:
                if para.text.strip():
                    md_content += para.text + "\n\n"
                    
            self._save_md_and_archive(filepath, md_content)
        except Exception as e:
            print(f"❌ 워드 파싱 중 에러 발생: {e}")
            
    def _save_md_and_archive(self, orig_path, md_content):
        # 1. 마크다운 파일로 저장 (temp 폴더 내에 저장하면 watchdog이 다시 감지하여 A-Wiki를 호출함)
        new_md_path = orig_path.with_suffix('.md')
        with open(new_md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ 마크다운 변환 완료: {new_md_path.name}")
        
        # 2. 원본 파일은 Archive로 이동 (충돌 방지를 위해 약간 대기)
        try:
            time.sleep(1)
            shutil.move(str(orig_path), os.path.join(ARCHIVE_DIR, orig_path.name))
            print(f"📦 원본 아카이빙 완료: {ARCHIVE_DIR}")
        except Exception as e:
            print(f"⚠️ 아카이빙 실패 (파일이 사용 중일 수 있음): {e}")

if __name__ == "__main__":
    event_handler = AWikiTrigger()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"🛡️ 아위키 옴니보어(잡식성) 핫폴더 모니터링 시작: {WATCH_DIR}")
    print("지원 확장자: .md, .xlsx, .docx")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
