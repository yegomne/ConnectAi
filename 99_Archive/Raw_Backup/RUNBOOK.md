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
