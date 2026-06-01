# 실행 매뉴얼 & 트러블슈팅 (Runbook)

> 사장님이 반복 작업하실 때 보는 문서. 명령어 복붙용.

---

## 1. 일상 실행 절차

### 1-1. 매번 작업 시작 시

```powershell
# 1. 프로젝트 폴더로 이동
cd "E:\성인용품 등록 반자동화\adult_product_renamer"

# 2. 가상환경 활성화
..\venv\Scripts\activate
# 또는 (venv 위치에 따라)
.venv\Scripts\activate

# 3. 세컨 PC 연결 확인
python -m tests.test_connection
```

연결 OK 메시지 + 모델 6개 표시되면 정상.

### 1-2. 상품명 리네이밍 실행

```powershell
python tests/test_renamer.py
```

기본은 `samples/input_samples.txt`의 샘플을 처리.

### 1-3. 새 상품 추가해서 테스트

`samples/input_samples.txt` 편집:
```
# 카테고리힌트 필요 없는 경우 (정보가 충분한 상품명)
A-123 [BRAND] 상품명 모델번호

# 카테고리힌트 필요한 경우 (모델 코드만 있는 경우)
B-456 X-789 | 여성 섹시 란제리 검정 레이스 팬티
```

---

## 2. 세컨 PC 사전 설정 (재부팅 후 또는 신규 환경)

### 2-1. Ollama가 외부 연결 받게 설정

세컨 PC PowerShell **관리자 권한**:

```powershell
# 환경변수 영구 설정
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "Machine")

# 확인
[Environment]::GetEnvironmentVariable("OLLAMA_HOST", "Machine")
```

### 2-2. 방화벽 열기 (한 번만)

세컨 PC PowerShell **관리자 권한**:

```powershell
# 기존 규칙 확인
Get-NetFirewallRule -DisplayName "*Ollama*" -ErrorAction SilentlyContinue

# 없으면 추가
New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow -Profile Any
```

### 2-3. Ollama 재시작 (환경변수 적용)

```powershell
Get-Process ollama* | Stop-Process -Force
Start-Sleep -Seconds 2
Start-Process "ollama" -ArgumentList "serve"
```

또는 트레이 아이콘 우클릭 → Quit Ollama → 시작 메뉴에서 다시 실행.

### 2-4. 동작 확인

세컨 PC 자체:
```powershell
curl http://127.0.0.1:11434/api/tags
curl http://192.168.0.200:11434/api/tags  # 자기 외부 IP로도 확인
```

메인 PC에서:
```powershell
curl http://192.168.0.200:11434/api/tags
```

세 경우 모두 JSON으로 모델 리스트 나와야 정상.

---

## 3. Ollama 모델 관리

### 3-1. 현재 설치 모델 확인

세컨 PC:
```powershell
ollama list
```

### 3-2. 권장 모델 다운로드

```powershell
# 메인 (확정 사용)
ollama pull qwen3:14b

# 비전 (4단계용)
ollama pull llama3.2-vision

# 비교용 (선택)
ollama pull exaone3.5:7.8b
```

### 3-3. 불필요 모델 삭제

VRAM 초과로 사용 못 하는 모델 (디스크 40GB 확보):
```powershell
ollama rm qwen3.6:27b
ollama rm qwen3.6:35b-a3b
```

### 3-4. 모델 워밍업 (선택)

첫 호출이 느리므로 미리 GPU에 로드:
```powershell
ollama run qwen3:14b "hi"
```

---

## 4. 트러블슈팅

### 4-1. "Connection refused" / WinError 10061

**증상**: 메인 PC에서 세컨 PC 접속 실패

**진단 순서**

1. **세컨 PC 켜져 있는지** (당연하지만 한 번 확인)
   ```powershell
   ping 192.168.0.200
   ```

2. **Ollama가 외부 IP를 듣고 있는지**
   세컨 PC에서:
   ```powershell
   netstat -ano | findstr 11434
   ```
   결과가 `0.0.0.0:11434` 이어야 정상.
   `127.0.0.1:11434` 이면 → 2-1 (OLLAMA_HOST) 재설정

3. **방화벽 차단 여부**
   세컨 PC에서 위 2-2 명령 확인

4. **IP 자체 변경 여부**
   세컨 PC에서:
   ```powershell
   ipconfig | findstr IPv4
   ```
   `192.168.0.200`이 아니면 → `.env` 파일의 `SECOND_PC_IP` 수정

---

### 4-2. UnicodeEncodeError (cp949 / 이모지)

**증상**: 콘솔에 ✅ 같은 이모지 출력 시 에러

**해결**: 스크립트 최상단에 추가
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

`test_renamer.py`엔 이미 적용됨. 새 스크립트 만들 때 빼먹지 말 것.

---

### 4-3. 응답이 빈 JSON `{}` 으로 옴

**증상**: LLM 응답이 0.4초 만에 끝나고 내용 없음

**원인**: qwen3 thinking 모드 비활성화 + JSON 강제 충돌

**해결**
- `src/prompts.py` 에 `/no_think` 가 있으면 제거
- `src/ollama_client.py` 의 페이로드에 `"think": false` (또는 명시 안 함)
- 단, qwen3 14b/8b에서는 빈 응답 발생 시 자동 재시도 + thinking 켜고 폴백 로직이 있음 (현재 코드 적용 완료)

---

### 4-4. 응답이 60초 이상 걸리고 타임아웃

**증상**: `Ollama 추론이 60초 내에 끝나지 않았습니다` 에러

**원인**: VRAM 부족 → 일부 CPU 처리 → 3 tok/s로 추락

**진단**: 세컨 PC에서
```powershell
ollama run qwen3:14b "안녕" --verbose
```
응답 끝에 표시되는 `eval rate`를 확인:
- 60+ tok/s → 정상
- 30~60 tok/s → 약간 부족
- 10 미만 → VRAM 초과, **즉시 작은 모델로 교체**

**해결**
- 더 작은 양자화 버전 다운로드 (`qwen3:14b-q4_K_M` 등이 존재한다면)
- 또는 `qwen3:8b`로 다운그레이드 (품질 손해)
- 또는 `.env`의 `REQUEST_TIMEOUT`을 180으로 늘리기 (임시방편)

---

### 4-5. requirements.txt를 찾을 수 없음

**증상**: `ERROR: Could not open requirements file`

**원인**: 현재 폴더 오인

**해결**
```powershell
# 현재 위치 확인
pwd

# 프로젝트 폴더로 이동 (한글 + 공백 폴더 주의)
cd "E:\성인용품 등록 반자동화\adult_product_renamer"

# 파일 존재 확인
dir requirements.txt

# 그 다음 설치
pip install -r requirements.txt
```

---

### 4-6. PowerShell 실행 정책 에러 (가상환경 활성화 실패)

**증상**: `Activate.ps1 cannot be loaded because running scripts is disabled`

**해결**: PowerShell 관리자 권한으로
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

### 4-7. 카테고리 오염이 의심되는 결과

**증상**: 여성용 상품에 "명기" 같은 남성 키워드, 또는 반대

**확인**
- `test_renamer.py` 출력에서 `└ 자동교정:` 라인 확인
- 자동 교정이 적용됐는데도 오염 남아있으면 → `src/validator.py`의 `CATEGORY_REPLACEMENT_MAP`에 매핑 추가 필요

**예시 추가**
```python
CATEGORY_REPLACEMENT_MAP["새카테고리"] = {
    "오염키워드1": "허용키워드1",
    "오염키워드2": "허용키워드2",
}
```

---

## 5. 안티그래비티 + Claude Code 워크플로우

### 5-1. 새 기능 추가 시 표준 순서

1. 안티그래비티 IDE에서 작업 폴더 열기 (`E:\성인용품 등록 반자동화\`)
2. 터미널 열기 (`Ctrl + ~`)
3. `claude` 실행 (Claude Code 시작)
4. 명확한 프롬프트 작성 → 입력
5. 권한 요청 시 `y` (자동 진행)
6. 작업 완료 메시지 대기
7. `Ctrl + C` 또는 `/exit`로 Claude Code 빠져나오기
8. 일반 터미널에서 테스트 실행

### 5-2. Claude Code 프롬프트 작성 가이드

좋은 프롬프트의 구조:
```
# 프로젝트: [한 줄 설명]
## 배경
## 환경 정보 (세컨 PC IP 등)
## 핵심 요구사항 (파일별)
## 작업 순서
## 코드 품질 요건
## 하지 말아야 할 것
```

PROJECT.md를 매번 첨부할 필요는 없으나, 큰 단계 시작 시엔 첨부 권장.

---

## 6. 자주 쓰는 단축 명령

### 6-1. 연결만 빠르게 확인
```powershell
python -m tests.test_connection
```

### 6-2. 샘플 1개만 빠르게 테스트
```powershell
# samples/input_samples.txt에 한 줄만 남기고 실행
python tests/test_renamer.py
```

### 6-3. 모델만 바꿔서 비교 테스트
`.env` 파일에서 `MODEL_NAME=qwen3:14b` 부분만 다른 모델로 변경 후 재실행.

### 6-4. 프롬프트 미세 조정
`src/prompts.py` 의 `RENAME_PROMPT_TEMPLATE` 수정 → 저장 → `test_renamer.py` 재실행.
재시작/재컴파일 불필요.

---

## 7. 정기 점검 체크리스트 (월 1회)

- [ ] `ollama list` — 모델 다 있는지
- [ ] `python -m tests.test_connection` — 연결 정상
- [ ] `python tests/test_renamer.py` — 30개 후보 100% 통과
- [ ] 새로운 카테고리 상품 만나면 `CATEGORY_REPLACEMENT_MAP`에 추가
- [ ] 쿠팡/네이버 정책 변경 모니터링 — 금칙어 사전 업데이트
- [ ] 사용 안 하는 모델 삭제로 디스크 정리

---

## 8. 비상 연락처 / 참고 자료

- Ollama 공식 문서: https://ollama.com/library
- qwen3 모델 페이지: https://ollama.com/library/qwen3
- Anthropic Claude API: https://docs.claude.com
- 본 프로젝트 의사결정 기록: `DECISIONS.md`
- 본 프로젝트 개요: `PROJECT.md`

---

# 2단계: FastAPI 서버 운영

---

## 7. 네트워크 드라이브 (Z:\) 관리

### 7-1. 매핑 상태 확인

메인 PC PowerShell:
```powershell
# Z 드라이브 보이는지
dir Z:\

# 또는 매핑된 모든 네트워크 드라이브 확인
Get-PSDrive -PSProvider FileSystem
```

### 7-2. 매핑 끊겼을 때 (재부팅 후 등)

메인 PC PowerShell:
```powershell
New-PSDrive -Name "Z" `
            -PSProvider FileSystem `
            -Root "\\192.168.0.200\renamer" `
            -Credential "yegom\pthem" `
            -Persist
```

비밀번호 입력창 뜨면 세컨 PC `pthem` 계정 비밀번호 입력.

### 7-3. 매핑 해제 (재구성 필요 시)

```powershell
Remove-PSDrive -Name "Z"
# 또는 net use 사용
net use Z: /delete
```

### 7-4. 세컨 PC 측 공유 상태 확인

세컨 PC PowerShell:
```powershell
Get-SmbShare -Name "renamer"

# 활성 연결 확인 (메인 PC가 보여야 함)
Get-SmbSession
```

---

## 8. FastAPI 서버 운영

### 8-1. 서버 시작 (세컨 PC, 매 작업 시)

```powershell
# 세컨 PC에서 (파섹 접속)
cd C:\Users\pthem\Documents\adult_product_renamer
.\venv\Scripts\activate
python src\server.py
```

성공 시 다음과 같은 로그가 떠야 함:
```
INFO: [모델 워밍업] qwen3:14b 첫 로딩 중...
INFO: [모델 워밍업] 완료. 응답 8.3초
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**이 터미널 창은 계속 켜둬야 함.** 닫으면 서버 죽음.

### 8-2. 서버 동작 확인 (3가지 방법)

**방법 A: 브라우저 (가장 편함)**

메인 PC 브라우저에서:
```
http://192.168.0.200:8000/docs
```

Swagger UI 페이지 뜨면 OK.

**방법 B: PowerShell**

```powershell
# 인증 없으니 -UseBasicParsing 추가하면 경고 없음
curl http://192.168.0.200:8000/health -UseBasicParsing
```

또는 JSON 객체로 파싱:
```powershell
Invoke-RestMethod http://192.168.0.200:8000/health
```

**방법 C: Python**

```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
python -c "import requests; print(requests.get('http://192.168.0.200:8000/health').json())"
```

### 8-3. 실제 리네이밍 호출 (테스트)

**Swagger UI에서 (권장)**
1. 브라우저로 `http://192.168.0.200:8000/docs`
2. `POST /rename` 펼치기
3. `Try it out` 버튼
4. Request body:
   ```json
   {
     "original_name": "C-915 [N.P.G] 명기의증명 016",
     "category_hint": ""
   }
   ```
5. `Execute` 클릭

**Python으로 (배치 처리 시)**
```python
import requests
response = requests.post(
    "http://192.168.0.200:8000/rename",
    json={
        "original_name": "C-915 [N.P.G] 명기의증명 016",
        "category_hint": ""
    }
)
print(response.json())
```

### 8-4. 회귀 테스트 (변경사항 검증)

코드 수정 후 항상 6개 카테고리 회귀 테스트로 검증:

**메인 PC에서**
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
$env:API_BASE_URL = "http://192.168.0.200:8000"
python Z:\tests\test_api.py
```

**세컨 PC에서 (간편)**
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
.\venv\Scripts\activate
python tests\test_api.py
```

기대 결과: 6개 카테고리 × 5후보 = 30개 후보 모두 ✅ 또는 자동 교정 처리됨.

### 8-5. 서버 종료

서버 떠 있는 터미널에서 `Ctrl + C`. 깔끔하게 셧다운됨.

### 8-6. 서버 재시작 (코드 수정 후)

`server.py`나 `prompts.py` 등 수정 시 서버 재시작 필요:
```powershell
# 1. Ctrl+C로 기존 서버 종료
# 2. 다시 실행
python src\server.py
```

> 참고: uvicorn `--reload` 옵션은 사용 안 함. reload는 모델을 매번 재로딩해서 워밍업 비용 증가.

---

## 9. FastAPI 트러블슈팅

### 9-1. "원격 서버에 연결할 수 없습니다" / Connection refused

**원인 후보**
1. 세컨 PC에서 서버가 안 켜져 있음 → 가장 흔함
2. 서버는 떴는데 0.0.0.0이 아닌 127.0.0.1로 바인딩됨
3. 방화벽이 8000 포트 차단

**진단**

세컨 PC에서:
```powershell
# 서버 프로세스 확인
Get-Process python | Where-Object {$_.MainWindowTitle -match "uvicorn"}

# 포트 8000 듣고 있는지
netstat -ano | findstr 8000
```

결과가 `0.0.0.0:8000 LISTENING` 이어야 정상. `127.0.0.1:8000`이면 외부 거부.

**해결**: `src/server.py`의 uvicorn 실행 부분 확인:
```python
uvicorn.run("server:app", host="0.0.0.0", port=8000, ...)
```

`host="0.0.0.0"` 필수.

**방화벽 추가 (한 번만)**

세컨 PC PowerShell 관리자:
```powershell
New-NetFirewallRule -DisplayName "FastAPI-8000" `
                    -Direction Inbound `
                    -Protocol TCP `
                    -LocalPort 8000 `
                    -Action Allow -Profile Any
```

### 9-2. PowerShell 응답 한글 깨짐

**증상**: `Invoke-RestMethod` 결과의 한글이 `ëªê¸°` 처럼 깨져 보임

**원인**: PowerShell이 응답 디코딩 시 인코딩 추측 실패. 콘솔 인코딩 설정도 이미 깨진 데이터는 복구 불가.

**해결 방법 3가지 (우선순위 순)**

**방법 1: Swagger UI 사용 (가장 쉬움)**
```
http://192.168.0.200:8000/docs
```
브라우저는 한글 완벽 처리.

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

**방법 3: Python 사용 (가장 정공법)**
test_api.py 같은 Python 스크립트는 첫 줄에 `sys.stdout.reconfigure(encoding='utf-8')` 들어가 있어 한글 정상.

### 9-3. 응답 시간이 갑자기 느려짐 (30초 이상)

**가능성 1**: 모델이 메모리에서 언로드됨 (keep_alive 만료)

server.py 호출 페이로드에 `"keep_alive": "30m"` 들어있는지 확인. 30분 이상 호출 없으면 GPU에서 내려감 → 첫 호출 워밍업 필요.

**가능성 2**: 세컨 PC에 다른 무거운 작업 중

세컨 PC `nvidia-smi` 확인. GPU 점유율 90%+ 다른 작업 있으면 LLM 추론 양보.

**가능성 3**: 네트워크 일시 불안정

```powershell
ping 192.168.0.200 -n 20
```
패킷 손실 확인.

### 9-4. JSON 파싱 실패 (502 Bad Gateway)

**증상**: `/rename` 호출 시 502 에러

**원인**: Ollama 응답이 JSON 아닌 경우 (모델이 thinking 모드 끄고 빈 응답 등)

**해결**: 1단계 D-003 참조. `src/prompts.py`에 `/no_think` 없는지 + ollama_client.py에서 thinking 정식 옵션 사용 중인지 확인.

---

## 10. 자주 쓰는 단축 명령 (2단계)

### 10-1. 서버 상태 30초 점검
```powershell
# 1. Z 드라이브 매핑 확인
dir Z:\ -ErrorAction SilentlyContinue

# 2. 서버 헬스
curl http://192.168.0.200:8000/health -UseBasicParsing

# 3. 단건 테스트 (Swagger UI 권장)
start http://192.168.0.200:8000/docs
```

### 10-2. 전체 회귀 테스트
```powershell
cd "E:\성인용품 등록 반자동화"
.\.venv\Scripts\activate
$env:API_BASE_URL = "http://192.168.0.200:8000"
python Z:\tests\test_api.py
```

### 10-3. 서버 로그 보기 (세컨 PC)
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
Get-Content server.log -Tail 50 -Wait
```

---

## 11. 정기 점검 체크리스트 (월 1회)

기존 1단계 체크리스트에 추가:

- [ ] FastAPI 서버 uptime 확인 (`/health`의 `uptime_seconds`)
- [ ] `total_requests` 카운터 증가 추이
- [ ] `server.log` 크기 확인 (10MB 넘으면 로테이션)
- [ ] Z:\ 드라이브 정상 매핑 (`dir Z:\`)
- [ ] 세컨 PC 디스크 여유 (`Get-PSDrive C`)
- [ ] CORS 정책 점검 (외부 노출 시작했다면 `*` 제거)

---

## 12. 운영 자동화 로드맵 (7단계)

현재는 세컨 PC 재부팅 시 사장님이 수동으로 서버 시작.
자동화 옵션:

### 12-1. 작업 스케줄러 등록 (권장)

세컨 PC에서:
```powershell
$action = New-ScheduledTaskAction `
    -Execute "C:\Users\pthem\Documents\adult_product_renamer\venv\Scripts\python.exe" `
    -Argument "C:\Users\pthem\Documents\adult_product_renamer\src\server.py" `
    -WorkingDirectory "C:\Users\pthem\Documents\adult_product_renamer"

$trigger = New-ScheduledTaskTrigger -AtStartup

Register-ScheduledTask -TaskName "FastAPI-Renamer" `
                      -Action $action `
                      -Trigger $trigger `
                      -RunLevel Highest `
                      -User "yegom\pthem"
```

### 12-2. NSSM으로 Windows 서비스화 (대안)

```powershell
# NSSM 설치 후
nssm install FastAPI-Renamer "C:\Users\pthem\Documents\adult_product_renamer\venv\Scripts\python.exe" "C:\Users\pthem\Documents\adult_product_renamer\src\server.py"
nssm start FastAPI-Renamer
```

> 채택 시점: 3·4단계 완료 후 1주일 무사고 운영 시점에 적용.
