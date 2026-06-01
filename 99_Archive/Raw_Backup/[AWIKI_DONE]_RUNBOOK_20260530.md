# 실행 매뉴얼 & 트러블슈팅 (Runbook)

> 사장님이 반복 작업하실 때 보는 문서. 명령어 복붙용.

---

# 1단계: 상품명 리네이머 CLI

---

## 1. 일상 실행 절차 (1단계 CLI)

### 1-1. 매번 작업 시작 시

```powershell
# 1. 프로젝트 폴더로 이동
cd "E:\성인용품 등록 반자동화"

# 2. 가상환경 활성화
.\.venv\Scripts\activate

# 3. 세컨 PC 연결 확인
cd adult_product_renamer
python -m tests.test_connection
```

### 1-2. CLI 회귀 테스트
```powershell
python tests\test_renamer.py
```

`samples/input_samples.txt`의 6개 샘플 처리.

---

## 2. 세컨 PC 사전 설정 (재부팅 후 또는 신규 환경)

### 2-1. Ollama 외부 연결 설정

세컨 PC PowerShell **관리자 권한**:

```powershell
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "Machine")
[Environment]::GetEnvironmentVariable("OLLAMA_HOST", "Machine")
```

### 2-2. 방화벽 (한 번만)

```powershell
Enable-NetFirewallRule -DisplayGroup "파일 및 프린터 공유"

New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound `
                    -Protocol TCP -LocalPort 11434 `
                    -Action Allow -Profile Any
```

### 2-3. Ollama 재시작

```powershell
Get-Process ollama* | Stop-Process -Force
Start-Sleep -Seconds 2
Start-Process "ollama" -ArgumentList "serve"
```

### 2-4. 동작 확인

```powershell
curl http://127.0.0.1:11434/api/tags
curl http://192.168.0.200:11434/api/tags
```

---

## 3. Ollama 모델 관리

### 3-1. 현재 설치 모델
```powershell
ollama list
```

### 3-2. 권장 모델 다운로드
```powershell
ollama pull qwen3:14b          # 메인 (1·2·3단계)
ollama pull llama3.2-vision    # 4단계용
```

### 3-3. 불필요 모델 삭제 (40GB 확보)
```powershell
ollama rm qwen3.6:27b
ollama rm qwen3.6:35b-a3b
```

### 3-4. 모델 워밍업
```powershell
ollama run qwen3:14b "hi"
```

---

## 4. 트러블슈팅 (공통)

### 4-1. "Connection refused" / WinError 10061

**진단**
1. 세컨 PC 켜져있는지: `ping 192.168.0.200`
2. Ollama 외부 IP 듣고 있는지 (세컨 PC):
   ```powershell
   netstat -ano | findstr 11434
   ```
   `0.0.0.0:11434 LISTENING` 정상 / `127.0.0.1:11434` 외부 거부

**해결**: 2-1 (OLLAMA_HOST) 재설정 → 2-3 (재시작)

### 4-2. UnicodeEncodeError (cp949 / 이모지)

스크립트 최상단 추가:
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 4-3. 응답이 빈 JSON `{}`

**원인**: qwen3 thinking 비활성화 + JSON 강제 충돌

**해결**: 
- `src/prompts.py`에 `/no_think` 없는지 확인
- `src/ollama_client.py`에서 thinking 정식 옵션 사용 중인지 확인

### 4-4. 60초 타임아웃

**원인**: VRAM 부족 (eval rate 3 tok/s 추락)

**진단**: 세컨 PC에서
```powershell
ollama run qwen3:14b "안녕" --verbose
```
`eval rate` 확인. 30 미만이면 VRAM 부족 확정.

**해결**: 더 작은 모델로 교체, 또는 `REQUEST_TIMEOUT=180`으로 임시방편

### 4-5. requirements.txt 못 찾음

```powershell
pwd
cd "E:\성인용품 등록 반자동화\adult_product_renamer"
dir requirements.txt
pip install -r requirements.txt
```

### 4-6. PowerShell 실행 정책

관리자 권한:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 4-7. 카테고리 오염 자동 교정 안 됨

`src/validator.py`의 `CATEGORY_REPLACEMENT_MAP`에 매핑 추가:
```python
CATEGORY_REPLACEMENT_MAP["새카테고리"] = {
    "오염키워드1": "허용키워드1",
}
```

---

# 2단계: FastAPI 서버 운영

---

## 5. 네트워크 드라이브 (Z:\) 관리

### 5-1. 매핑 상태 확인
```powershell
dir Z:\
Get-PSDrive -PSProvider FileSystem
```

### 5-2. 매핑 끊겼을 때 (재부팅 후 등)
```powershell
New-PSDrive -Name "Z" `
            -PSProvider FileSystem `
            -Root "\\192.168.0.200\renamer" `
            -Credential "yegom\pthem" `
            -Persist
```

### 5-3. 매핑 해제
```powershell
Remove-PSDrive -Name "Z"
net use Z: /delete
```

### 5-4. 세컨 PC 측 공유 상태
```powershell
Get-SmbShare -Name "renamer"
Get-SmbSession  # 연결 확인
```

---

## 6. FastAPI 서버 운영

### 6-1. 서버 시작 (세컨 PC, 매 작업 시)
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
.\venv\Scripts\activate
python src\server.py
```

성공 메시지:
```
INFO: [모델 워밍업] qwen3:14b 첫 로딩 중...
INFO: [모델 워밍업] 완료. 응답 8.3초
INFO: Uvicorn running on http://0.0.0.0:8000
```

**터미널 켜둔 채로 유지**.

### 6-2. 서버 동작 확인

**브라우저 (가장 편함)**
```
http://192.168.0.200:8000/docs
```

**PowerShell**
```powershell
curl http://192.168.0.200:8000/health -UseBasicParsing
```

**Python**
```powershell
python -c "import requests; print(requests.get('http://192.168.0.200:8000/health').json())"
```

### 6-3. Swagger UI 사용
1. 브라우저로 `/docs` 접속
2. `POST /rename` → `Try it out`
3. Request body:
   ```json
   {"original_name": "C-915 [N.P.G] 명기의증명 016", "category_hint": ""}
   ```
4. `Execute`

### 6-4. 회귀 테스트

**세컨 PC** (가장 간편):
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
.\venv\Scripts\activate
python tests\test_api.py
```

**메인 PC**:
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
$env:API_BASE_URL = "http://192.168.0.200:8000"
python Z:\tests\test_api.py
```

### 6-5. 서버 종료
서버 떠 있는 터미널에서 `Ctrl + C`.

### 6-6. 서버 재시작 (코드 수정 후)
1. `Ctrl + C` 종료
2. `python src\server.py` 재실행

---

## 7. FastAPI 트러블슈팅

### 7-1. "원격 서버에 연결할 수 없습니다"

**진단**: 세컨 PC에서
```powershell
netstat -ano | findstr 8000
```
`0.0.0.0:8000` 정상 / `127.0.0.1:8000` 외부 거부

**해결**: `src/server.py` uvicorn 실행부 `host="0.0.0.0"` 확인

**방화벽 추가**:
```powershell
New-NetFirewallRule -DisplayName "FastAPI-8000" `
                    -Direction Inbound -Protocol TCP `
                    -LocalPort 8000 -Action Allow -Profile Any
```

### 7-2. PowerShell 응답 한글 깨짐

**증상**: `Invoke-RestMethod` 결과의 한글이 `ëªê¸°` 같이 깨짐

**해결 (우선순위 순)**

**방법 1: Swagger UI**
```
http://192.168.0.200:8000/docs
```

**방법 2: 수동 UTF-8 디코딩**
```powershell
$body = @{original_name="C-915 [N.P.G] 명기의증명 016"; category_hint=""} | ConvertTo-Json
$response = Invoke-WebRequest -Uri http://192.168.0.200:8000/rename `
                              -Method POST -Body $body `
                              -ContentType "application/json; charset=utf-8"
$json = [System.Text.Encoding]::UTF8.GetString($response.RawContentStream.ToArray())
$data = $json | ConvertFrom-Json
$data.candidates | ForEach-Object { Write-Host "($($_.length)자) $($_.text)" }
```

**방법 3: Python**
`test_api.py` 같이 `sys.stdout.reconfigure(encoding='utf-8')` 적용된 스크립트 사용.

### 7-3. 응답 시간 30초+

**원인 1**: 모델 메모리에서 언로드됨 (keep_alive 만료)
- `src/ollama_client.py`에 `"keep_alive": "30m"` 확인

**원인 2**: 세컨 PC 다른 작업 중
- 세컨 PC `nvidia-smi` 확인

**원인 3**: 네트워크 일시 불안정
```powershell
ping 192.168.0.200 -n 20
```

### 7-4. 502 Bad Gateway (JSON 파싱 실패)
**원인**: qwen3 thinking 모드 충돌
**해결**: 4-3 참조

---

# 3단계: Streamlit GUI 운영

---

## 8. GUI 첫 실행 설정 (한 번만)

### 8-1. 메인 PC 의존성 설치
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
cd adult_product_renamer
pip install -r requirements.txt
```

streamlit 설치 1~2분 소요.

### 8-2. 폴더 구조 확인
```powershell
dir gui
dir data
```

`gui/`: app.py, api_client.py, storage.py, keyword_extractor.py, categories.py, components.py  
`data/`: db_schema.sql, exports/

---

## 9. GUI 일상 실행

### 9-1. 매번 작업 시작

**전제 조건**: 세컨 PC FastAPI 서버 가동 중

**메인 PC에서 GUI 실행 (2가지 방법)**

**방법 A: 더블클릭 (가장 편함)**
- `E:\성인용품 등록 반자동화\run_gui.bat` 더블클릭
- 브라우저 자동으로 `http://localhost:8501` 열림

**방법 B: 명령어**
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
streamlit run adult_product_renamer\gui\app.py
```

### 9-2. GUI 작업 흐름

1. 상품명 입력 (필수)
2. 대분류·소분류 선택 (선택, 강화학습 데이터 분류용)
3. 카테고리힌트 입력 (선택)
4. [후보 생성] 클릭 → 8초 대기
5. 5개 후보 카드 중 선택 → 자동 저장
   - 또는 6번째 카드(직접 조립) 키워드 클릭으로 만들기
6. [다음 상품] 또는 사이드바 [✨ 새 상품]

### 9-3. 6번째 카드 사용 팁

- **녹색 박스 (이전 키워드)**: 같은 카테고리 재방문 시 자동 표시. 클릭으로 추가
- **6분류 칩**: 5개 후보에서 추출. 핵심/카테고리/스펙/형용사/부스터/용도
- **빈도순 전체 (접힌 상태)**: 펼쳐서 빈도순 확인
- **새 키워드 추가**: 텍스트박스 + [추가] 버튼. 자유 키워드 등록
- **직접 편집**: 조립 텍스트박스에서 타이핑·삭제·순서 변경 가능
- ⚠️ **글자수 카운터**: 직접 타이핑 시 즉시 갱신 안 됨 (Enter 또는 클릭 시 갱신). 50자 초과 시 결정 버튼 비활성화

### 9-4. GUI 종료

GUI 떠 있는 터미널에서 `Ctrl + C`. 브라우저 닫아도 서버는 살아있음.

---

## 10. GUI 트러블슈팅

### 10-1. "❌ 서버 연결 실패" 사이드바 표시

**원인**: 세컨 PC FastAPI 서버 안 켜짐

**해결**: 세컨 PC에서 6-1 (서버 시작)

### 10-2. 키워드 칩 클릭 반응 없음

**원인**: Streamlit 버튼 클릭 신호 소실 (이미 페이즈 2.5에서 해결됨)

**확인**: `gui/components.py`에서 모든 버튼이 `on_click` 콜백 방식인지

### 10-3. 글자수 카운터 즉시 안 바뀜

**원인**: Streamlit `text_input`의 기본 동작 (D-028)

**대응**: 
- Enter 또는 다른 곳 클릭 시 갱신됨 (정상)
- 키워드 칩 클릭은 즉시 반응
- 50자 초과 시 결정 버튼 비활성화 (안전망 작동)

### 10-4. 처리 이력 안 보임

**원인**: SQLite DB 파일 권한 또는 경로 문제

**진단**:
```powershell
dir adult_product_renamer\data\history.db
```

파일 없으면 자동 생성됨 (첫 저장 시). 있으면 권한 확인:
```powershell
icacls adult_product_renamer\data\history.db
```

### 10-5. Streamlit 포트 충돌

**증상**: `Address already in use`

**해결**: 다른 포트로 실행
```powershell
streamlit run adult_product_renamer\gui\app.py --server.port 8502
```

또는 기존 프로세스 종료:
```powershell
Get-Process streamlit | Stop-Process -Force
```

### 10-6. 브라우저 자동 안 열림

**원인**: Streamlit 설정 또는 기본 브라우저 미설정

**해결**: 수동으로 `http://localhost:8501` 접속

또는 `.streamlit/config.toml` 생성:
```toml
[server]
headless = false
[browser]
serverAddress = "localhost"
serverPort = 8501
```

---

## 11. 자주 쓰는 단축 명령

### 11-1. 서버 상태 30초 점검
```powershell
# 1. Z 드라이브
dir Z:\

# 2. FastAPI 서버
curl http://192.168.0.200:8000/health -UseBasicParsing

# 3. Swagger UI
start http://192.168.0.200:8000/docs
```

### 11-2. 전체 회귀 테스트
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
$env:API_BASE_URL = "http://192.168.0.200:8000"
python Z:\tests\test_api.py
```

### 11-3. GUI 즉시 실행
```powershell
# E:\성인용품 등록 반자동화\ 폴더에서 (탐색기)
.\run_gui.bat
```

### 11-4. 서버 로그 확인 (세컨 PC)
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
Get-Content server.log -Tail 50 -Wait
```

### 11-5. DB 백업
```powershell
copy "adult_product_renamer\data\history.db" `
     "adult_product_renamer\data\history_backup_$(Get-Date -Format 'yyyyMMdd').db"
```

---

## 12. 정기 점검 체크리스트 (월 1회)

- [ ] FastAPI 서버 uptime (`/health`의 `uptime_seconds`)
- [ ] `total_requests` 카운터 추이
- [ ] `server.log` 크기 (10MB 넘으면 로테이션)
- [ ] Z:\ 드라이브 매핑 (`dir Z:\`)
- [ ] 세컨 PC 디스크 여유 (`Get-PSDrive C`)
- [ ] SQLite DB 크기 (`history.db`)
- [ ] DB 백업 (월 1회)
- [ ] 강화학습 데이터 통계
  ```sql
  SELECT category_key, COUNT(*) FROM category_keywords GROUP BY category_key;
  ```

---

## 13. 운영 자동화 로드맵 (7단계)

### 13-1. 작업 스케줄러 등록 (FastAPI 자동 시작)

세컨 PC에서:
```powershell
$action = New-ScheduledTaskAction `
    -Execute "C:\Users\pthem\Documents\adult_product_renamer\venv\Scripts\python.exe" `
    -Argument "C:\Users\pthem\Documents\adult_product_renamer\src\server.py" `
    -WorkingDirectory "C:\Users\pthem\Documents\adult_product_renamer"

$trigger = New-ScheduledTaskTrigger -AtStartup

Register-ScheduledTask -TaskName "FastAPI-Renamer" `
                      -Action $action -Trigger $trigger `
                      -RunLevel Highest -User "yegom\pthem"
```

### 13-2. NSSM Windows 서비스 (대안)

```powershell
nssm install FastAPI-Renamer `
    "C:\Users\pthem\Documents\adult_product_renamer\venv\Scripts\python.exe" `
    "C:\Users\pthem\Documents\adult_product_renamer\src\server.py"
nssm start FastAPI-Renamer
```

채택 시점: 3·4단계 완료 후 1주일 무사고 운영 시점.

---

## 14. 안티그래비티 + Claude Code 워크플로우

### 14-1. 새 기능 추가 표준 순서

1. 안티그래비티 IDE 열기 → 작업 폴더 (`E:\성인용품 등록 반자동화\` 또는 `Z:\`)
2. 터미널 (`Ctrl + ~`) → `claude` 실행
3. 명확한 프롬프트 작성 → 입력
4. 권한 요청 `y`로 진행
5. 작업 완료 대기
6. `Ctrl + C` 또는 `/exit`로 Claude Code 빠져나오기
7. 일반 터미널에서 테스트 실행

### 14-2. 프롬프트 작성 구조

```
# 프로젝트: [한 줄 설명]
## 배경
## 환경 정보 (세컨 PC IP, 경로 등)
## 핵심 요구사항 (파일별)
## 작업 순서
## 코드 품질 요건
## 하지 말아야 할 것
```

큰 단계 시작 시엔 `PROJECT.md` + 관련 `PHASE*.md` 첨부 권장.

---

## 15. 비상 연락처 / 참고 자료

- Ollama 공식: https://ollama.com/library
- qwen3 모델: https://ollama.com/library/qwen3
- Streamlit 공식: https://docs.streamlit.io
- FastAPI 공식: https://fastapi.tiangolo.com
- 본 프로젝트 의사결정: `DECISIONS.md`
- 본 프로젝트 개요: `PROJECT.md`
- 2단계 상세: `PHASE2_FASTAPI.md`
- 3단계 상세: `PHASE3_STREAMLIT.md`
