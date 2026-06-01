# 2단계: FastAPI 서버화 — 상세 기록

> 작업 일자: 2026-05-29
> 소요 시간: 약 2시간 (페이즈 0 ~ 페이즈 3)
> 검증 결과: 30개 후보 100% 통과, 1단계와 동등 품질

---

## 1. 작업 목적

1단계는 CLI(`python tests/test_renamer.py`)로만 동작. 이를 HTTP API로 노출해서:

1. **모델 로딩 비용 제거** — 매 실행 시 발생하던 5~10초 워밍업을 서버 시작 시 1회만 발생
2. **GUI 통합 준비** — 3단계 GUI가 HTTP 요청만 보내면 됨 (Python import 불필요)
3. **외부 도구 연동** — curl, Postman, n8n 등에서 호출 가능
4. **메인-세컨 역할 분리** — 메인 PC GUI는 가벼움, 세컨 PC가 GPU 작업 전담

---

## 2. 페이즈 진행 기록

### 페이즈 0: 네트워크 드라이브 매핑

#### 작업 내용
- 세컨 PC에 작업 폴더 생성: `C:\Users\pthem\Documents\adult_product_renamer`
- SMB 공유 설정: 공유명 `renamer`, 권한 `yegom\pthem` Full Access
- 메인 PC에서 Z:\에 영구 매핑 (`-Persist` 옵션)

#### 사용 명령어

세컨 PC (관리자 PowerShell):
```powershell
New-SmbShare -Name "renamer" `
             -Path "C:\Users\pthem\Documents\adult_product_renamer" `
             -FullAccess "yegom\pthem"

Enable-NetFirewallRule -DisplayGroup "파일 및 프린터 공유"
```

메인 PC:
```powershell
New-PSDrive -Name "Z" `
            -PSProvider FileSystem `
            -Root "\\192.168.0.200\renamer" `
            -Credential "yegom\pthem" `
            -Persist
```

#### 결과
- 메인 PC `Z:\` = 세컨 PC 작업 폴더, 즉시 동기화
- 메인 PC에서 안티그래비티로 Z:\ 폴더 열면 세컨 PC 코드 직접 편집 가능

#### 학습 포인트
- venv는 **PC 종속적이라 동기화 X**: robocopy에 `/XD .venv` 옵션 필수
- SMB 인증 정보는 Windows 자격증명 관리자에 저장됨 (재부팅 후 자동 재연결)

---

### 페이즈 1: FastAPI 코드 작성

#### 산출 파일

| 파일 | 역할 |
|---|---|
| `src/server.py` | FastAPI 애플리케이션 (신규) |
| `tests/test_api.py` | HTTP 호출 회귀 테스트 (신규) |
| `requirements.txt` | fastapi, uvicorn, pydantic 추가 |
| `README.md` | 서버 실행/테스트 섹션 추가 |
| `.gitignore` | `*.log` 추가 |

#### 작업 방식
- 안티그래비티에서 Z:\ 폴더 열기 → 메인 PC에서 편집하지만 세컨 PC 파일에 직접 반영
- Claude Code(claude-code CLI)에 통합 프롬프트 던지고 자동 생성
- 1단계 코드(`renamer.py`, `validator.py`, `prompts.py`, `ollama_client.py`) **절대 수정 안 함** → `from src.renamer import Renamer`로 import만

#### server.py 핵심 구조

```python
# 1. lifespan으로 서버 시작 시 Renamer 인스턴스 생성 + 모델 워밍업
@asynccontextmanager
async def lifespan(app: FastAPI):
    global renamer
    renamer = Renamer(OllamaClient())
    # 워밍업: 더미 요청 1회로 GPU에 모델 로드
    renamer.ollama_client.generate(prompt="안녕", format="")
    yield

# 2. /health: 서버·Ollama 상태
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "ollama_connected": ...,
        "model": "qwen3:14b",
        "uptime_seconds": ...,
        "total_requests": ...
    }

# 3. /rename: 핵심 엔드포인트
@app.post("/rename")
async def rename(request: RenameRequest) -> RenameResponse:
    result = renamer.rename(request.original_name, request.category_hint)
    return RenameResponse(**result)
```

#### Pydantic 스키마

요청:
```python
class RenameRequest(BaseModel):
    original_name: str
    category_hint: str = ""
```

응답:
```python
class CandidateInfo(BaseModel):
    text: str
    length: int
    length_ok: bool
    too_short: bool
    too_long: bool
    forbidden_words: list[str]
    category_pollutions_before: list[str]
    category_pollutions_after: list[str]
    auto_fixes: list[str]
    deduped_words: list[str]
    booster_added: list[str]
    llm_original_text: str

class RenameResponse(BaseModel):
    original: str
    category_hint: str
    candidates: list[CandidateInfo]
    elapsed_seconds: float
    model: str
    warnings: list[str]
```

#### CORS
내부망 전용이지만 GUI 개발 편의상 모든 origin 허용:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

### 페이즈 2: 서버 띄우고 테스트

#### 세컨 PC 환경 구성
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### 서버 실행
```powershell
python src\server.py
```

uvicorn이 띄움. 첫 워밍업 8.3초 후:
```
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 메인 PC 첫 호출 (Swagger UI)
브라우저로 `http://192.168.0.200:8000/docs` → `POST /rename` Try it out:

```json
{
  "original_name": "C-915 [N.P.G] 명기의증명 016",
  "category_hint": ""
}
```

**결과**:
- HTTP 200
- elapsed_seconds: 7.109
- 5개 후보 모두 length_ok=true (35~38자)
- category_pollutions_after = [] (오염 없음)
- booster_added 다양화 작동 (어덜트굿즈/19금용품/성인전용/프리미엄/신상품)

---

### 페이즈 3: 회귀 테스트

#### test_api.py 환경변수 지원

기본 URL을 `localhost:8000`로 두되, 환경변수로 오버라이드 가능:
```python
BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
```

메인 PC에서 실행 시:
```powershell
$env:API_BASE_URL = "http://192.168.0.200:8000"
python Z:\tests\test_api.py
```

#### 회귀 테스트 결과

6개 카테고리 모두 1단계와 **동등 품질** 확인:

| 카테고리 | 원본 | 응답 시간 | 결과 |
|---|---|---|---|
| 남성 명기 | C-915 [N.P.G] 명기의증명 016 | 7.7초 | 5/5 ✅ |
| 남성 매트 | E-480 [YEAIN]용봉매트2세대... | 9.0초 | 5/5 ✅ |
| 여성 바이브 | H-1462 [LILO]터치다운 지스팟 | 7.9초 | 5/5 ✅ |
| 애널/후방 | M-314 [LILO]블랙미사일K | 8.2초 | 5/5 ✅ (자동 교정) |
| 란제리 | L-828 A-T512 | 10.4초 | 5/5 ✅ |
| 커플 수갑 | Q-405 엑스원 수갑 (대) | 8.5초 | 5/5 ✅ |

**총 30개 후보 100% 통과.**

특히 M-314 (애널) 카테고리에서 LLM이 또 "명기" 키워드를 출력했지만, 1단계에서 만든 `auto_fix_category_pollution` 후처리가 5/5 모두 "후방"으로 교정. **1단계 안전망이 그대로 작동**.

---

## 3. 트러블슈팅 기록

### 트러블 1: PowerShell 인코딩 에러 (인지된 문제)

**증상**:
```
.\.venv\Scripts\activate
'.\.venv\Scripts\activate' 용어가 cmdlet, 함수, 스크립트 파일 ... 인식되지 않습니다.
```

**원인**: venv가 다른 위치(상위 폴더 `E:\성인용품 등록 반자동화\.venv\`)에 있음. 1단계 작업 초기에 만든 venv 위치를 기억해야 함.

**해결**: 상위 폴더로 이동 후 활성화.

---

### 트러블 2: test_api.py가 localhost:8000 보고 있음

**증상**:
```
[설정] API 베이스 URL: http://localhost:8000
[치명적] 서버(http://localhost:8000)에 연결할 수 없습니다.
```

**원인**: Claude Code가 기본값을 `localhost:8000`으로 둠. 메인 PC에서 실행 시 자기 자신을 보게 됨.

**해결**: 환경변수 사용 (`$env:API_BASE_URL = "http://192.168.0.200:8000"`).

---

### 트러블 3: Invoke-RestMethod 한글 깨짐

**증상**: API 응답이 `ëªê¸°ìì¦ëª` 같은 깨진 한글로 출력.

**원인**: PowerShell이 응답 바디 디코딩 시 인코딩 추측 실패. 콘솔 인코딩 설정해도 이미 깨진 데이터는 복구 불가.

**해결책 (3가지 우선순위)**:
1. **Swagger UI 사용** — 브라우저는 UTF-8 완벽 처리
2. `Invoke-WebRequest` + `[System.Text.Encoding]::UTF8.GetString()` 수동 디코딩
3. Python 스크립트 사용 (test_api.py는 `sys.stdout.reconfigure(encoding='utf-8')` 적용됨)

**채택**: Python으로 자동화, Swagger UI로 수동 검증. PowerShell 직접 호출은 권장 안 함.

---

### 트러블 4: 첫 호출 12.47초 → 두 번째 7.1초

**증상**: 첫 호출이 두 번째보다 5초 이상 느림.

**원인**: 모델 워밍업. lifespan에서 워밍업 호출했지만, 실제 추론 요청 시 모델 GPU 상태가 약간 다름.

**해결**: 정상 동작. 운영 시엔 첫 호출 후 안정. keep_alive=30m으로 30분간 메모리 유지.

---

## 4. 검증된 운영 메트릭

### 응답 시간 분포
- 평균: 8.6초
- 최소: 7.1초
- 최대: 10.4초 (란제리 카테고리, 카테고리힌트 길어서 토큰 증가)
- 95퍼센타일: ~10초

### 안정성
- 2시간+ uptime, 메모리 누수 없음
- JSON 파싱 실패: 0회
- 자동 교정 작동: 정상

### 자원 사용
- 메인 PC: 거의 0 (HTTP 요청만 보냄)
- 세컨 PC GPU VRAM: ~9GB (qwen3:14b 상주)
- 세컨 PC RAM: ~1GB (FastAPI + Python)
- 네트워크 대역폭: 요청 ~200B, 응답 ~2KB (무시할 수준)

---

## 5. 미완료 작업 / 향후 개선점

### 즉시 추가 가능
- [ ] `POST /rename/batch` — 여러 상품명 동시 처리 엔드포인트
- [ ] `/metrics` — Prometheus 형식 메트릭 (요청 카운트, 응답 시간 히스토그램)
- [ ] 요청 ID(X-Request-ID) 헤더 응답에 포함 (이미 일부 구현됨)

### 7단계로 미룬 것
- [ ] 작업 스케줄러로 부팅 시 자동 시작
- [ ] 로그 로테이션 (server.log)
- [ ] 헬스체크 실패 시 알림 (이메일·슬랙 등)

### 4단계 통합 시 추가
- [ ] `POST /classify_image` — llama3.2-vision NSFW 분류
- [ ] `POST /extract_subject` — BiRefNet 누끼 추출
- [ ] 파일 업로드 (Base64 vs 경로 전달 결정 필요)

---

## 6. 다음 단계(3단계 GUI) 준비 사항

### API 사용 예시 코드 (3단계 GUI 작성자용)

```python
import requests

API_BASE = "http://192.168.0.200:8000"

# 1. 헬스체크
def is_server_alive() -> bool:
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        return r.status_code == 200 and r.json().get("status") == "ok"
    except:
        return False

# 2. 상품명 리네이밍
def rename_product(original: str, category_hint: str = "") -> dict:
    response = requests.post(
        f"{API_BASE}/rename",
        json={
            "original_name": original,
            "category_hint": category_hint
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()

# 3. 사용 예
result = rename_product("C-915 [N.P.G] 명기의증명 016")
for i, candidate in enumerate(result["candidates"], 1):
    marker = "✅" if candidate["length_ok"] else "⚠️"
    print(f"{i}. {marker} ({candidate['length']}자) {candidate['text']}")
```

### Streamlit GUI 예상 구조 (참고)

```python
import streamlit as st
import requests

st.title("성인용품 SEO 리네이머")

original = st.text_input("원본 상품명")
category_hint = st.text_input("카테고리 힌트 (선택)")

if st.button("후보 생성"):
    with st.spinner("리네이밍 중... (8초)"):
        result = requests.post(
            "http://192.168.0.200:8000/rename",
            json={"original_name": original, "category_hint": category_hint}
        ).json()
    
    for i, c in enumerate(result["candidates"], 1):
        if st.button(f"{i}. ({c['length']}자) {c['text']}", key=f"pick_{i}"):
            st.success(f"선택됨: {c['text']}")
            # 여기서 SQLite 저장 + 엑셀 추가
```

50줄 정도면 단건 검수 GUI 완성. 이미지 표시·이력 검색 추가하면 100줄.

---

## 7. 이 단계에서 깨달은 것

### 사장님 우려: "웹이라 느려지나?"

명확히 검증됨:
- HTTP 통신 시간: 0.002초 (내부망 2.5Gbps)
- 전체 응답의 99.97%는 LLM 추론
- FastAPI 오버헤드는 무시할 수준

### FastAPI의 진짜 가치
- API 노출은 부수 효과
- 진짜 가치는 **모델 로딩 비용 제거** (5~10초 워밍업이 매 실행 → 서버 시작 1회)
- GUI 통합 시 Python import 불필요해서 메인 PC 가벼움

### LLM 응용 개발의 안전망 재확인
1단계에서 만든 후처리(자동 교정, 부스터, 중복 제거)가 2단계 API 호출에서도 그대로 작동.
**LLM이 같은 실수를 또 했음에도(M-314 "명기")** 5/5 자동 교정 성공.

**교훈**: LLM 프롬프트는 80% 보장, 코드 후처리가 나머지 20% 강제. 둘 다 필요.

### 인프라 작업의 함정 4종 경험
1. venv 위치 오인 (PC별 종속)
2. PowerShell 인코딩 4중 함정 (요청·응답·콘솔·디코딩)
3. localhost vs 외부 IP 구분 (테스트 스크립트 환경변수화)
4. 네트워크 드라이브 권한 (Full Access 명시 필수)

이 4가지는 다음 단계에서도 반복될 가능성 큼 → RUNBOOK.md 섹션 9 참고.
