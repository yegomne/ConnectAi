# 3단계: Streamlit GUI — 상세 기록

> 작업 일자: 2026-05-30
> 진행 상황: **페이즈 0 ~ 3.5 완료 (3단계 GUI 전체 완성)**
> 검증 결과: 메인 + 이력 + 통계 + 엑셀 모두 작동. 텍스트박스 실시간 갱신만 제한 (수용)

---

## 1. 작업 목적

1·2단계 완료 시점:
- ✅ 1단계: 상품명 리네이밍 로직 (`Renamer` 클래스)
- ✅ 2단계: FastAPI 서버 (`POST /rename` 엔드포인트)

3단계가 만드는 것:
- **사장님이 마우스 클릭만으로 단건 검수하는 GUI**
- 메인 PC에서 실행, 브라우저로 띄움
- API 호출만 함 (Streamlit이 GUI, FastAPI가 두뇌)

---

## 2. 핵심 컨셉 — 강화학습형 단건 검수

D-022 결정: **현재 LLM 방식 유지 + 6번째 카드 직접 조립 + 강화학습 누적**

### 시간에 따른 작동 방식

```
[Day 1]
상품명 입력 → 5개 후보 (LLM 추측, 일부 환각 가능)
       ↓
사장님이 6번째 카드에서 키워드 클릭 + 직접 입력
       ↓
이 작업 자체가 강화학습 데이터로 저장됨

[Day 7]
같은 카테고리 새 상품 입력
       ↓
6번째 카드 → "이전에 사용한 키워드" 자동 표시
       ↓
클릭만으로 조립 빨라짐

[Day 30]
"이전에 사용한 키워드"가 풍부해짐
       ↓
강화학습 데이터 → LLM 프롬프트에 자동 주입 (4단계에서 구현)
       ↓
5개 후보 자체가 사장님 스타일로 진화 → 환각 자연 감소

[Day 90, 4단계 통합 시]
비전 모델 추가 → 자동 키워드 추출
       ↓
사장님은 확인·수정만
```

**핵심 가치**: 사장님 도매 노하우가 시스템에 자동 누적되는 휴먼 인 더 루프 학습.

---

## 3. 페이즈 진행 기록

### 페이즈 0: 환경 준비 ✅

#### 작업 내용
- 폴더 구조 생성: `gui/`, `data/`, `gui/pages/`
- 의존성 추가: `streamlit>=1.32.0`, `openpyxl>=3.1.0`, `pandas>=2.0.0`
- 카테고리 마스터 (`gui/categories.py`): 리보스 사이트 실제 트리 7대분류 × 27소분류
- SQLite 스키마 (`data/db_schema.sql`): `history`, `category_keywords` 2개 테이블
- 실행 스크립트 (`run_gui.bat`): 메인 PC 더블클릭 실행

#### 카테고리 마스터 데이터
사장님이 직접 보내주신 리보스 사이트 캡처 기반:

| 대분류 | 소분류 |
|---|---|
| 남성용품 코너 | 남성명품관, 리얼돌, 남성홀컵, 자동핸드잡(홀), 남성바디자동, 남성바디수동, 중형바디, 핸드잡소형, 특수점보실리콘, 진동링/강화링, 일반보조링, 단련/확장기 |
| 여성용품 코너 | 여성명품관, 페어리진동기, 회전형진동기, 일체형진동기, 분리형진동기, 리얼진동먹쇠, 리얼수동먹쇠, 대물먹쇠/전시물 |
| 애널용품 코너 | 진동애널, 수동애널 |
| 콘돔용품 코너 | 국산콘돔, 수입/초박형콘돔 |
| 맛사지젤/향수 코너 | 기능맛사지젤, 고급맛사지젤, 페로몬향수, 세정제/기타 |
| 섹시속옷/란제리 코너 | JSP섹시란제리, 여성섹시팬티, 남성섹시팬티, 섹시망사/스타킹, 섹시란제리, 섹시코스프레, 섹시가터벨트 |
| SM용품 코너 | 목줄/수갑/족갑, 자갈/바디구속, 채찍/가면/안대 |

#### SQLite 스키마 핵심

```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    original_name TEXT NOT NULL,
    category_key TEXT NOT NULL,
    category_hint TEXT DEFAULT '',
    selected_text TEXT NOT NULL,
    selected_index INTEGER NOT NULL,        -- 1~5: LLM, 6: 직접 조립
    selected_keywords_json TEXT DEFAULT '', -- 6번 카드에서 클릭한 키워드 순서
    all_candidates_json TEXT NOT NULL,
    elapsed_seconds REAL DEFAULT 0,
    model TEXT DEFAULT 'qwen3:14b'
);

CREATE TABLE category_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_key TEXT NOT NULL,
    keyword TEXT NOT NULL,
    source TEXT NOT NULL,                   -- 'manual' / 'llm' / 'spec'
    first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    use_count INTEGER DEFAULT 1,
    is_blocked BOOLEAN DEFAULT 0,
    UNIQUE(category_key, keyword)
);
```

---

### 페이즈 1: 데이터 계층 ✅

#### 산출 파일

| 파일 | 역할 |
|---|---|
| `gui/api_client.py` | FastAPI 호출 + 에러 처리 |
| `gui/storage.py` | SQLite 입출력 + 강화학습 |
| `gui/keyword_extractor.py` | 5개 후보 → 6분류 키워드 |
| `tests/test_gui_modules.py` | 단독 테스트 스크립트 |

#### api_client.py 핵심

```python
class ApiClient:
    def __init__(self, base_url: str = "http://192.168.0.200:8000"):
        self.base_url = base_url
        self.timeout = 90
    
    def health(self) -> dict: ...
    def is_alive(self) -> bool: ...
    def rename(self, original_name: str, category_hint: str = "") -> dict: ...

@dataclass
class ApiError(Exception):
    message: str
    status_code: Optional[int] = None
```

#### storage.py 주요 함수

**이력 관리**
- `save_history(...)`: 처리 결과 저장
- `find_history_by_original(original_name)`: 중복 체크
- `get_recent_history(limit)`: 사이드바 표시용
- `search_history(keyword, category_key)`: 이력 페이지 검색
- `get_history_count()`: 통계 (오늘/누적/평균 응답)

**강화학습 관리**
- `record_keyword_usage(category_key, keywords, source)`: UPSERT로 사용 횟수 누적
- `get_top_keywords(category_key, limit)`: 빈도순 추천 키워드
- `block_keyword/unblock_keyword`: 차단 관리

**SQLite UPSERT 패턴** (강화학습 핵심)
```python
conn.execute("""
    INSERT INTO category_keywords (category_key, keyword, source)
    VALUES (?, ?, ?)
    ON CONFLICT(category_key, keyword) DO UPDATE SET
        use_count = use_count + 1,
        last_used_at = CURRENT_TIMESTAMP
""", (category_key, kw, source))
```

#### keyword_extractor.py 6분류 로직

```python
def classify_keyword(word: str, original_name: str) -> str:
    if word in original_name: return "core"        # 원본 유래
    if word in BOOSTER_KEYWORDS: return "booster"
    if word in USAGE_KEYWORDS: return "usage"
    if word in ADJECTIVE_KEYWORDS: return "adjective"
    if re.search(r'\d+', word): return "spec"
    if word in SPEC_KEYWORDS: return "spec"
    if word in CATEGORY_KEYWORDS: return "category"
    if word.endswith(("한", "운", "는")): return "adjective"
    return "category"
```

복합 키워드 보존 처리 (`"혼자 즐기는"` 같은 띄어쓰기 포함 키워드):
```python
def split_to_words(text: str) -> list[str]:
    # 복합 키워드를 임시 토큰으로 치환 후 공백 분할 → 다시 복원
    ...
```

#### 페이즈 1 테스트 결과

```
[1] ApiClient 테스트
  서버 URL: http://192.168.0.200:8000
  [OK] 서버 응답: model=qwen3:14b, uptime=11883s
  [OK] 후보 5개 받음, 응답시간 12.531초

[2] keyword_extractor 테스트
  - core (원본 유래): ['명기', 'C-915', '016']
  - category:        ['남성용품', '솔로용품', '진동기구']
  - spec:            ['리얼터치', '6피스톤', '진동']
  - booster:         ['어덜트굿즈', '19금용품', '성인전용', '프리미엄']
  - 빈도 top 5: 명기 x5, 리얼터치 x5, C-915 x5, 016 x5, 남성용품 x5

[3] storage 테스트
  [OK] 이력 저장됨, id=1
  [OK] 동일 상품명 이력 1건 발견
  [OK] 강화학습 추천: 정숙형 x2, 명기 x1, 리얼터치 x1, ...
```

UPSERT 동작 검증: "정숙형" 첫 호출 1, 두 번째 호출 +1 → x2 정확.

---

### 페이즈 2: 메인 화면 ✅

#### 산출 파일

| 파일 | 역할 |
|---|---|
| `gui/app.py` | Streamlit 메인 페이지 |
| `gui/components.py` | 카드 컴포넌트 (LLM 후보, 직접 조립) |

#### 화면 구조

**사이드바**
- 시스템 상태 (서버 연결, 모델, uptime)
- 처리 통계 (오늘 / 누적 / 평균 응답)
- 최근 처리 5건 미리보기 (expander로 펼침)

**메인 화면 (위→아래)**
1. 제목 + 서버 상태 인디케이터 (🟢/🔴)
2. 입력 폼 (st.form 안에)
   - 원본 상품명 (필수)
   - 대분류 selectbox
   - 소분류 selectbox (대분류 선택 시 활성화)
   - 카테고리힌트 text_input
   - [✨ 후보 생성하기] 버튼
3. 중복 경고 (해당 시)
4. (API 응답 후) 5개 후보 카드 + 6번째 직접 조립 카드

#### 5개 후보 카드 (render_candidate_card)

```python
with st.container(border=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"**후보 {index}** · _{strategy}_  `{length}자`")
        st.write(text)
    with col2:
        clicked = st.button("✅ 선택", key=f"{key_prefix}_btn")
```

전략 라벨 5종 (1단계 D-005에서 정의):
1. 핵심키워드형
2. 기능강조형
3. 사용감강조형
4. 용도강조형
5. 롱테일형

#### 6번째 카드 (render_builder_card)

구조:
```
[💚 이 카테고리에서 자주 쓰신 키워드]  ← 강화학습 (사장님 입력 누적)
   [정숙형 ×8] [방수형 ×5] [충전식 ×4] ...
─────────────────────────────────────
[🏷️ 5개 후보에서 추출된 키워드]  ← 6분류
   📌 핵심: [명기의증명] [016]
   🎯 카테고리: [남성용품] [솔로용품]
   ⚡ 스펙: [10진동] [리얼터치]
   ✨ 형용사: [부드러운]
   🏷️ 부스터: [어덜트굿즈] [19금용품]
   🚫 용도: [혼자 즐기는]
─────────────────────────────────────
[📊 빈도순 전체 키워드 보기]  ← 접힌 상태
─────────────────────────────────────
[➕ 새 키워드 추가]
   [텍스트박스] [추가] 버튼
─────────────────────────────────────
[✏️ 조립된 상품명 (직접 편집 가능)]   29자 / 50자
   [텍스트박스 — 자유 편집 가능]
─────────────────────────────────────
[✅ 이 상품명으로 결정]  [🔄 초기화]
```

#### 페이즈 2 첫 테스트 결과

사장님이 직접 사용해보신 결과:

| 테스트 | 결과 |
|---|---|
| ✅ Streamlit 정상 실행, 브라우저 자동 열림 | 통과 |
| ✅ 5개 후보 카드 표시 + [선택] 버튼 | 통과 |
| ✅ 중복 경고 (같은 상품명 재입력 시) | 통과 |
| ✅ 사이드바 통계 갱신 | 통과 |
| ❌ 6번째 카드 키워드 클릭 반응 없음 | **페이즈 2.5에서 수정** |

스크린샷 첨부됨 — 메인 화면 디자인 깔끔하게 나옴.

#### 사장님 추가 요청
- "첫페이지에서 처리가 되면 중간에 다른 상품명을 넣을수 있게 처음화면으로 버튼"
→ 페이즈 2.5에서 추가

---

### 페이즈 2.5: 미세 조정 ✅

#### 해결한 문제 1: 키워드 클릭 반응 없음

**원인**: Streamlit `st.columns` 안의 `st.button`에서 `st.rerun()` 직접 호출 시 클릭 신호 소실

**해결**: 모든 키워드 버튼을 `on_click` 콜백 방식으로 변경

```python
def _on_keyword_click(keyword: str, kw_state_key: str, text_state_key: str):
    keywords = st.session_state.get(kw_state_key, [])
    keywords.append(keyword)
    st.session_state[kw_state_key] = keywords
    
    current = st.session_state.get(text_state_key, "")
    if current:
        st.session_state[text_state_key] = f"{current} {keyword}"
    else:
        st.session_state[text_state_key] = keyword

# 버튼 생성
st.button(
    word,
    key=f"{key_prefix}_{cat_id}_{i}",
    on_click=_on_keyword_click,
    args=(word, keywords_state_key, text_state_key),
    use_container_width=True,
)
```

**핵심**: `st.rerun()` 직접 호출 안 함. Streamlit이 콜백 후 자동 rerun.

#### 해결한 문제 2: 처음으로 버튼 부재

**추가 위치**
1. 5개 후보 화면 우측 상단: `[↶ 처음으로]`
2. 6번째 카드 아래: `[↶ 처음으로 돌아가기]`
3. 사이드바 맨 위: `[✨ 새 상품 입력]` (가장 편함)

**공통 동작**: `_reset_to_input()` 함수
```python
def _reset_to_input():
    st.session_state.api_result = None
    st.session_state.selected_done = False
    st.session_state.duplicate_warning_shown = False
    st.session_state.duplicate_proceed = False
    st.session_state.current_input_name = ""
    
    # 6번째 카드 state도 초기화
    for k in list(st.session_state.keys()):
        if k.startswith("builder_"):
            del st.session_state[k]
```

#### 페이즈 2.5 재테스트 결과

| 테스트 | 결과 |
|---|---|
| ✅ A. 키워드 클릭 작동 | 통과 |
| ✅ B. 직접 편집 (단, 글자수 실시간 갱신은 제한) | 통과 (제한 사항 수용) |
| ✅ C. 처음으로 버튼 (상단/하단/사이드바) | 통과 |
| ✅ D. 6번째 카드 결정 + 저장 | 통과 |

---

## 4. 알려진 제한 사항

### 텍스트박스 실시간 글자수 갱신 (D-028)

**현상**: 조립 텍스트박스에서 직접 타이핑 시 글자수 카운터 즉시 갱신 안 됨

**원인**: Streamlit `text_input` 위젯은 **blur(포커스 잃음) 시점 또는 Enter 키** 입력 시에만 서버에 값 전송. 타이핑 중에는 브라우저에만 값이 있음.

**검토한 해결책**
- A) 안내 문구만 표시 ← **채택**
- B) `text_area`로 변경
- C) HTML/JS 커스텀 컴포넌트 (진짜 실시간)
- D) 그냥 진행

**선택 근거**: A
- 사장님 주 작업은 키워드 칩 클릭 (이건 즉시 반응)
- 직접 타이핑은 보조 작업
- 결정 버튼 누르기 직전 blur 시점에 자동 갱신 + 50자 초과 시 비활성화 = 안전망 작동
- C는 ROI 낮음 (30분 작업 vs 페이즈 3 진행)

**사용자 영향**: 운영에 큰 지장 없음. 안내 문구 이미 표시됨.

---

## 5. 페이즈 3 + 3.5 완료 기록

### 페이즈 3: 이력 페이지 + 엑셀 + 키워드 통계 ✅

상위 Claude 모델(Opus 계열)로 Claude Code 작성. 의도·제약·검증 기준 중심 프롬프트 사용.
상위 모델이 기존 파일(storage.py 등)을 먼저 읽고 시그니처에 맞춰 작성 → 충돌 없음.

#### 5-1. 이력 페이지 (`gui/pages/1_📜_이력.py`)

- **혼합 표시**: 상단 `st.dataframe`(on_select="rerun", single-row) + 행 클릭 시 하단 카드 상세
- **필터**: 키워드 검색(원본+선택 LIKE), 카테고리 드롭다운, 기간 필터(체크박스 토글)
- **재선택**: 상세 카드에 5개 후보 전체 표시 → 다른 후보 클릭 시 `save_history()`로 **새 이력 INSERT** (기존 보존, 이력 추적성)
- **키워드 차단 (B2)**: 직접조립(6번) 이력의 사용 키워드를 버튼으로 나열, 클릭 시 `block_keyword()`
- **엑셀 다운로드**: on_click 콜백으로 export → download_button으로 다운로드
- 모든 상태 변경 버튼이 on_click 콜백 (페이즈 2.5 교훈 반영)

#### 5-2. 키워드 통계 페이지 (`gui/pages/2_📊_키워드_통계.py`) — 보너스 B1

- 탭 ① 카테고리별 TOP: expander + 막대 차트(상위 15, 차단 제외) + 표
- 탭 ② 전체 통합 TOP 30: 모든 카테고리 합산, 사장님 자주 쓰는 키워드
- 탭 ③ 차단 관리: 목록 + [차단 해제] 버튼

#### 5-3. 엑셀 출력 (`gui/excel_export.py`)

- `export_to_excel(history_rows, filename_prefix="result") -> Path`
- 2시트: "업로드용"(4컬럼) / "분석용"(9컬럼)
- 헤더 스타일(굵게+배경색), `_display_width()`로 한글 폭 고려 컬럼 너비 자동
- `_as_list()`로 JSON 문자열/list 양쪽 안전 처리
- 파일명 `result_YYYYMMDD_HHMMSS.xlsx`, `data/exports/`에 저장

#### 5-4. storage.py 추가 함수 (통계 페이지용 조회)

상위 모델이 관심사 분리 원칙 지켜서 SQL을 storage.py에만 작성:

```python
def get_all_keyword_stats(include_blocked: bool = True) -> dict[str, list[dict]]
    # 카테고리별 키워드 전체 (통계 탭 ①)
def get_overall_top_keywords(limit: int = 30, include_blocked: bool = False) -> list[dict]
    # 전 카테고리 통합 TOP (통계 탭 ②), total_count/category_count 집계
def get_blocked_keywords() -> list[dict]
    # 차단된 키워드 전체 (통계 탭 ③)
```

기존 함수(save_history, search_history, block_keyword 등)는 재작성 없이 호출만.

#### 페이즈 3 검증 결과
- 이력 테이블 → 행 클릭 → 상세 카드 → 재선택 정상
- 키워드 차단 → 통계 페이지 차단 목록 표시 + 해제 정상
- 엑셀 2시트 생성, 한글 안 깨짐
- 통계 3개 탭 정상 렌더링

---

### 페이즈 3.5: 6번째 카드 키워드 토글 ✅

#### 문제
키워드 칩 클릭 시 무조건 추가만 됨. 같은 칩 다시 눌러도 제거 안 되고 중복 추가.
사장님 지적: "잘못 선택했을 때 다시 누르면 없어져야 하는데 계속 추가됨"

#### 결정: 방식 A (순수 토글)

**고려한 후보**
- A) 순수 토글 (클릭=추가, 다시 클릭=제거) ← 채택
- B) 추가 전용 + 별도 되돌리기 버튼

**근거**
- 사장님 표현 "다시 누르면 없어져야"가 정확히 토글
- 같은 키워드 2번 넣기는 직접 편집 텍스트박스로 처리
- 칩 = "이 키워드 쓸지 말지" 스위치 역할

#### 구현 핵심

```python
def _on_keyword_toggle(keyword, kw_state_key, text_state_key):
    keywords = st.session_state.get(kw_state_key, [])
    if keyword in keywords:
        keywords = [k for k in keywords if k != keyword]  # 제거
    else:
        keywords = keywords + [keyword]                    # 추가
    st.session_state[kw_state_key] = keywords
    st.session_state[text_state_key] = " ".join(keywords)  # 리스트로부터 재생성
```

- **keywords 리스트를 단일 진실 소스(SSOT)** — 텍스트는 항상 리스트로부터 재생성
- 문자열 replace 안 씀 (부분일치 오류 위험)
- 선택된 칩은 `✓ {word}` + `type="primary"`로 시각 강조

#### 검증
사장님 직접 확인 — "아직 이상 안 보임". 토글 정상 작동.

---

## 6. (구) 페이즈 3 계획 — 완료됨

위 5장으로 모두 구현 완료. 통합 테스트는 1주일 실사용으로 대체 (사장님 결정).

---

## 6. 다음 단계(4단계) 준비 사항

### 비전 모델 통합 시 고려할 점

#### llama3.2-vision 추가 엔드포인트

```python
@app.post("/classify_image")
async def classify_image(file: UploadFile) -> ClassifyResponse:
    """이미지 NSFW 분류 (🟢🟡🔴)."""
    
@app.post("/extract_features")
async def extract_features(file: UploadFile, category_key: str) -> FeaturesResponse:
    """이미지에서 색상/사이즈/소재 등 자동 추출."""
```

#### 강화학습 데이터의 LLM 통합

`gui/storage.get_top_keywords()` 결과를 FastAPI `/rename` 호출 시 자동 포함:

```python
# FastAPI 측 prompts.py 갱신
prompt += f"""
[이 카테고리에서 사장님이 자주 쓰시는 키워드]
{', '.join(top_keywords)}

→ 위 키워드들을 최대한 활용해서 5개 후보를 생성하세요.
"""
```

**조건**: 누적 데이터가 카테고리당 10건+ 쌓이면 활성화.

---

## 7. 페이즈별 시간 통계

| 페이즈 | 작업 사이클 | 소요 시간 | 비고 |
|---|---|---|---|
| 페이즈 0 | 1회 | 5분 | 폴더, 의존성, 카테고리 마스터 |
| 페이즈 1 | 1회 | 30분 | 데이터 계층 3개 모듈 |
| 페이즈 2 | 1회 | 40분 | 메인 화면 + 컴포넌트 |
| 페이즈 2.5 | 1회 | 20분 | 키워드 클릭 수정 + 처음으로 버튼 |
| **합계** | **4회** | **약 1시간 35분** | |

1단계(8 사이클) 대비 작업 효율 매우 높아짐. 이유:
- 1·2단계에서 인프라(서버, DB, API) 다 갖춰진 상태
- Claude Code 프롬프트 정형화
- 사장님 요구사항 명확화

---

## 8. 이 단계에서 깨달은 것

### 사장님 통찰의 진화

1단계: "상품명만으로는 부족"
→ 카테고리힌트 도입 (D-004)

2단계: "웹이라 느려지나?"
→ FastAPI의 진짜 가치는 모델 로딩 비용 제거 (D-018)

3단계: "전문가로서 보기에 들어가선 안될 것들이 보여"
→ 6번째 카드 + 강화학습 (D-022)

3단계 추가: "제품마다 특징이 있어서 제품을 보면서 해야 함"
→ 카테고리 사전 운영 중 학습 (D-024)

3단계 추가: "강화학습이 있어서 그래"
→ 옵션 B 선택의 진짜 이유 = 시간이 해결

### Streamlit 함정 학습

1. **st.columns + st.button + st.rerun()**: 클릭 신호 소실 → `on_click` 콜백 사용
2. **text_input 실시간 갱신**: 불가능 (blur 시점만 전달)
3. **Session State 초기화**: 화면 전환 시 builder_* 키 명시적 삭제 필요
4. **버튼 key**: `f"{key_prefix}_{i}"` 패턴으로 충돌 방지

### 휴먼 인 더 루프 시스템의 설계

핵심 원리: **사람이 일을 할수록 시스템이 똑똑해진다**

```
사장님이 입력한 키워드 → category_keywords 누적
                       ↓
              다음 처리 시 추천 (UI)
                       ↓
                4단계에서 LLM 프롬프트 주입
                       ↓
                5개 후보 자체가 진화
                       ↓
                사장님이 또 입력
                       ↓
                  (선순환)
```

이건 1단계에서 의도하지 않았던 부수 효과인데, 3단계에서 사장님 의견("강화학습")으로 명시화됨. **사용자 의견이 아키텍처를 진화시킨 사례**.

---

## 9. 4단계 진입 전 체크리스트

페이즈 3 끝나면 다음 확인 후 4단계 진입:

- [ ] 페이즈 3 완료: 이력 페이지, 엑셀 출력, 통합 테스트
- [ ] 1주일 실사용: 사장님이 실제 도매 상품 등록 작업에 사용
- [ ] 강화학습 데이터 축적: 카테고리당 최소 5건+ 누적 확인
- [ ] 데이터 백업: `history.db` 백업 절차 검증
- [ ] 4단계 결정: 비전 모델 통합 방식 (API vs 파일 경로 전달)
- [ ] 모델 다운로드 점검: `llama3.2-vision` 동작 검증
