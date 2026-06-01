# 성인용품 등록 반자동화 프로젝트

> 마지막 업데이트: 2026-05-30
> 작업 위치: `E:\성인용품 등록 반자동화\`
> 현재 단계: **3단계 페이즈 2.5 완료** → 페이즈 3 (이력 페이지 + 엑셀 출력) 진입 직전

---

## 1. 프로젝트 목표

성인용품 도매몰(리보스)에서 받은 상품을 쿠팡·지마켓·옥션·11번가에 등록할 때 발생하는 두 가지 문제를 자동화로 해결한다.

### 문제 A: 노출 이미지 → 마켓 반려
- 공급사 이미지에 노출 부위 → 네이버 등 마켓 등록 반려
- → **포토샵으로 직접 처리** (자동 마스킹보다 빠름, 2분 내 완료)

### 문제 B: 아이템위너 경쟁 (쿠팡)
- 동일 공급사 → 셀러들이 같은 썸네일·상품명 사용 → 가격경쟁 마진 손실
- → **상품명 SEO 차별화 + 상세페이지 부분 누끼**로 독자성 확보

---

## 2. 시스템 환경

### 하드웨어 구성
| 항목 | 메인 PC | 세컨 PC (LLM + API 서버) |
|---|---|---|
| CPU | AMD Ryzen 5 7600 | AMD Ryzen 5 PRO 4650G |
| RAM | 32GB | 32GB |
| GPU | AMD Radeon RX 570 8GB | NVIDIA RTX 5060 Ti 16GB |
| IP | (DHCP) | **192.168.0.200** |
| 역할 | 개발 + GUI 실행 | Ollama + FastAPI 상시 가동 |

### 네트워크
- 두 PC 간 **2.5Gbps 내부망**
- 세컨 PC Ollama: `http://192.168.0.200:11434`
- 세컨 PC FastAPI: `http://192.168.0.200:8000`

### 네트워크 드라이브 (2단계 구축)
- 메인 PC `Z:\` ↔ 세컨 PC `C:\Users\pthem\Documents\adult_product_renamer\`
- SMB 공유명: `renamer`

### 개발 환경
- IDE: **구글 안티그래비티 (Antigravity)**
- AI 어시스턴트: **Claude Max**
- Python 3.10+ on Windows

---

## 3. 완료된 작업 — 1단계 (상품명 리네이머)

### 산출물
- 위치: `adult_product_renamer/src/` (메인 PC) ↔ 세컨 PC 동기화
- 기능: 공급사 원본 상품명 → SEO 상품명 5개 후보 자동 생성
- 사용 모델: **Ollama qwen3:14b** (세컨 PC, ~9GB VRAM)

### 검증 결과
- 6개 카테고리 × 5개 후보 = **30개 후보 100% 통과**
- 글자수 35~50자 준수, 카테고리 오염 자동 교정 작동

---

## 4. 완료된 작업 — 2단계 (FastAPI 서버화)

### 산출물
- `adult_product_renamer/src/server.py` — FastAPI 앱
- `adult_product_renamer/tests/test_api.py` — HTTP 회귀 테스트

### 엔드포인트
| 경로 | 메서드 | 기능 |
|---|---|---|
| `/` | GET | 서비스 메타 정보 |
| `/health` | GET | 서버·Ollama 상태, uptime, 총 요청 수 |
| `/rename` | POST | 상품명 1건 → SEO 후보 5개 (JSON) |
| `/docs` | GET | Swagger UI |

### 검증 결과
- 1단계 CLI와 동등 품질 (회귀 테스트 30/30)
- 평균 응답 8.6초 (FastAPI 오버헤드 0.5초 수준)
- Uptime 2시간+ 무사고 운영

상세: `PHASE2_FASTAPI.md`

---

## 5. 진행 중 — 3단계 (Streamlit GUI) ★ 페이즈 2.5 완료

### 산출물 (페이즈 0~2.5)
```
adult_product_renamer/
├── gui/
│   ├── __init__.py
│   ├── app.py                  # 메인 화면 (페이즈 2)
│   ├── api_client.py           # FastAPI 호출 래퍼 (페이즈 1)
│   ├── storage.py              # SQLite 입출력 (페이즈 1)
│   ├── keyword_extractor.py    # 5후보 → 6분류 키워드 (페이즈 1)
│   ├── categories.py           # 리보스 카테고리 마스터 (페이즈 0)
│   ├── components.py           # 카드 컴포넌트 (페이즈 2)
│   └── pages/
│       └── 1_📜_이력.py        # 이력 페이지 (페이즈 3 예정)
├── data/
│   ├── db_schema.sql           # SQLite 스키마
│   ├── history.db              # 처리 이력 DB (자동 생성)
│   └── exports/                # 엑셀 출력 폴더
└── run_gui.bat                 # 메인 PC 더블클릭 실행 (루트 폴더)
```

### 완료된 페이즈 (0~2.5)

#### 페이즈 0: 환경 준비 ✅
- 폴더 구조 생성 (`gui/`, `data/`, `pages/`)
- 의존성 설치 (`streamlit`, `openpyxl`, `pandas`)
- 리보스 카테고리 마스터 데이터 (7대분류 × 27소분류)
- SQLite 스키마 작성 (`history`, `category_keywords` 2개 테이블)
- `run_gui.bat` 실행 스크립트

#### 페이즈 1: 데이터 계층 ✅
- **api_client.py**: FastAPI 호출 + 에러 처리 (`ApiError` 예외)
- **storage.py**: 이력 저장, 중복 체크, 강화학습 키워드 누적
- **keyword_extractor.py**: 5개 후보 → 6분류 (core/category/spec/adjective/booster/usage) + 빈도순
- 단독 테스트 통과 (`tests/test_gui_modules.py`)

#### 페이즈 2: 메인 화면 ✅
- 입력 폼 (상품명 + 대/소분류 드롭다운 + 카테고리힌트)
- 5개 LLM 후보 카드 (전략 라벨 표시)
- 6번째 직접 조립 카드 (강화학습 키워드 + 6분류 칩 + 빈도순 전체)
- 사이드바: 시스템 상태, 처리 통계, 최근 5건
- 중복 입력 시 경고

#### 페이즈 2.5: 미세 조정 ✅
- 6번째 카드 키워드 클릭 반응 수정 (on_click 콜백 방식)
- 5개 후보 화면 상단/하단 [↶ 처음으로] 버튼
- 사이드바 [✨ 새 상품 입력] 단축 버튼

### 알려진 제한 사항 (개선 보류)

#### 텍스트박스 실시간 글자수 카운트
- **현상**: 직접 타이핑 시 글자수 카운터가 즉시 갱신 안 됨. 포커스 잃거나 Enter 누를 때 갱신
- **원인**: Streamlit `text_input` 위젯의 기본 동작
- **결정**: 안내 문구로 해결, HTML/JS 커스텀 컴포넌트는 ROI 낮아 보류
- **사용자 영향**: 키워드 칩 클릭은 실시간 반응. 직접 타이핑만 지연.
- **안전망**: 50자 초과 시 결정 버튼 자동 비활성화 (포커스 잃는 순간 검증)

### 페이즈 3 계획 (다음 작업)
- `gui/pages/1_📜_이력.py` — 처리 이력 검색·필터 페이지
- `gui/excel_export.py` — SQLite → xlsx 변환
- 이력 페이지 내 [엑셀 다운로드] 버튼
- 동일 상품명 재처리 시 이전 결과 보기 강화
- 6개 카테고리 실사용 통합 테스트

---

## 6. 시스템 아키텍처 (현재 상태)

```
[메인 PC]                              [세컨 PC: 192.168.0.200]
  │                                        │
  │ ┌─ E:\성인용품 등록 반자동화\          │
  │ │   adult_product_renamer\           │
  │ │   ├── src\          (1·2단계 코드) │
  │ │   ├── gui\          (3단계 GUI)    │
  │ │   ├── data\         (SQLite DB)    │
  │ │   └── ...                          │
  │ │                                    │
  │ └─ Z:\ (SMB) ─────────────────────► │ ┌─ C:\Users\pthem\Documents\
  │                                      │ │   adult_product_renamer\
  │                                      │ │   (코드 자동 동기화)
  │                                      │ │
  │ Streamlit GUI (:8501)                │ │ ┌─ FastAPI 서버 (:8000)
  │ ├─ 브라우저로 표시                   │ │ │  └─ Renamer (Python import)
  │ ├─ 사장님 작업                       │ │ │      └─ HTTP 요청
  │ └─ HTTP 요청                         │ │ │          ▼
  │      POST /rename ──────────────────►│ │ │      Ollama (:11434)
  │      약 8초 후 응답                  │ │ │      └─ qwen3:14b
  │      ◄─────────────────────────────  │ │ │         (메모리 상주)
  │                                      │ │ │
  │ SQLite 저장 (data/history.db)        │ │ │
  │ ├─ 이력                              │ │ │
  │ └─ 카테고리별 키워드 (강화학습)      │ │ │
```

---

## 7. 진행 계획 (다음 단계들)

### 3단계 마무리 — 페이즈 3 ← 다음 작업
이력 페이지, 엑셀 출력, 통합 테스트.

### 4단계: NSFW 스크리너 + 누끼 추출
- `llama3.2-vision`으로 이미지 분류 (🟢🟡🔴)
- 🔴 이미지를 별도 폴더로 자동 분리 → 포토샵 작업 대상 명확화
- BiRefNet으로 상세페이지 부분 누끼 → 1000×1000 흰배경 썸네일
- FastAPI에 엔드포인트 추가 (`POST /classify_image`, `POST /extract_subject`)

### 5단계: pHash 중복 검사 + 캐싱
- 공급사 동일 이미지 재사용 감지
- LLM 호출 캐싱으로 비용 절감

### 6단계 (보류): 마켓 자동 등록
- 단건 검수 업로드 방침이라 우선순위 낮음

### 7단계 (운영 안정화): 서버 자동 시작
- 작업 스케줄러로 세컨 PC 부팅 시 FastAPI 자동 가동
- 로그 로테이션

---

## 8. 보유 Ollama 모델 및 용도

세컨 PC `ollama list` 기준:

| 모델 | 크기 | 사용 단계 | 비고 |
|---|---|---|---|
| **qwen3:14b** | 9GB | **1·2·3단계 메인** | 상품명 리네이밍 (확정) |
| qwen3:8b | 5.2GB | 검증 후 탈락 | 백업/오프라인용 |
| qwen3-coder:30b | - | 미사용 | 안티그래비티 로컬 폴백 |
| qwen3.6:27b | 17GB | ❌ VRAM 초과 | **삭제 권장** |
| qwen3.6:35b-a3b | 23GB | ❌ VRAM 초과 | **삭제 권장** |
| llama3.2-vision | 7.8GB | 미사용 | **4단계 NSFW 스크리너** |
| gemma4:e4b | 9.6GB | 미사용 | 향후 가벼운 분류 작업 |

---

## 9. 핵심 기술 결정 사항 (요약)

상세는 `DECISIONS.md` 참조.

### 1단계 결정 (D-001 ~ D-013)
1. **모델: qwen3:14b** — 명령어 추종 + 한국어 + VRAM 적합
2. **thinking 모드 ON** — `/no_think` 사용 시 빈 JSON 버그
3. **카테고리힌트 입력 방식**
4. **자동 교정 후처리** — LLM 프롬프트만으론 카테고리 격리 불가
5. **단어 중복 제거 (max 2회)**
6. **이미지 마스킹 자동화 제외** — 포토샵이 더 빠름

### 2단계 결정 (D-014 ~ D-019)
7. **서버 구동: 수동 실행 → 자동 스케줄러 전환**
8. **코드 위치: 기존 프로젝트 내부 통합**
9. **동기화: SMB 네트워크 드라이브**
10. **인증: 없음 (내부망 전용)**
11. **FastAPI 부가 가치는 모델 로딩 비용 제거**
12. **회귀 테스트 의무화**

### 3단계 결정 (D-020 ~ D-028) ★ 신규
13. **GUI 프레임워크: Streamlit** (PyQt6 대신)
14. **GUI 실행 위치: 메인 PC**
15. **환각 처리: 6번째 카드 + 강화학습** (방향 C)
16. **카테고리 입력 UI: 드롭다운 추가** (강화학습 키)
17. **카테고리 사전: 옵션 B (운영 중 학습)**
18. **6번째 카드 키워드 분류: 옵션 C (카테고리 분류) + 옵션 B 보조**
19. **빼야 할 키워드: 옵션 A (즉시 토글)**
20. **6번째 카드 입력: 옵션 B (클릭 + 자유 편집)**
21. **글자수 제한: 50자 고정**
22. **저장 시 키워드 순서 기록**

---

## 10. 파일 구조 (현재 — 3단계 페이즈 2.5)

```
E:\성인용품 등록 반자동화\                          (메인 PC)
├── PROJECT.md                                    ← 이 문서
├── DECISIONS.md                                  ← 의사결정 (D-001 ~ D-028)
├── RUNBOOK.md                                    ← 실행·트러블슈팅
├── PHASE2_FASTAPI.md                             ← 2단계 상세
├── PHASE3_STREAMLIT.md                           ← 3단계 상세 ★ 신규
├── .venv\                                        ← Python venv
├── run_gui.bat                                   ← ★ GUI 더블클릭 실행
└── adult_product_renamer\
    ├── .env, .env.example, .gitignore
    ├── requirements.txt
    ├── README.md
    ├── src\                                      (1·2단계)
    │   ├── ollama_client.py
    │   ├── prompts.py
    │   ├── renamer.py
    │   ├── validator.py
    │   └── server.py
    ├── tests\
    │   ├── test_connection.py
    │   ├── test_renamer.py
    │   ├── test_api.py
    │   └── test_gui_modules.py                   ← 3단계 페이즈 1
    ├── samples\
    │   └── input_samples.txt
    ├── gui\                                      ★ 3단계 신규
    │   ├── __init__.py
    │   ├── app.py
    │   ├── api_client.py
    │   ├── storage.py
    │   ├── keyword_extractor.py
    │   ├── categories.py
    │   ├── components.py
    │   └── pages\
    │       └── (1_📜_이력.py — 페이즈 3 예정)
    └── data\                                     ★ 3단계 신규
        ├── db_schema.sql
        ├── history.db                            (자동 생성)
        └── exports\                              (엑셀 출력 폴더)
```

---

## 11. 다음 작업자(Claude) 인수인계

> 미래의 Claude가 이 프로젝트를 이어받을 때 읽을 섹션.

### 핵심 컨텍스트
- 사장님(`세현 사장님`)께 **항상 존댓말** 사용
- 사장님은 **단건 검수 업로드** 방식 선호 (대량 자동화 X)
- 이미지 마스킹은 **포토샵**으로 처리 (자동화 안 함)
- LLM 호출은 세컨 PC FastAPI 경유 (`http://192.168.0.200:8000`)
- GUI는 메인 PC Streamlit (`http://localhost:8501`)
- 강화학습: 사장님이 입력한 키워드가 다음 추천으로 누적

### 1·2·3단계에서 학습한 함정들 (다시 빠지지 말 것)
1. **qwen3 thinking 모드**: `/no_think` 지시자 + JSON 강제 = 빈 응답
2. **VRAM 초과**: 모델 선택 시 VRAM 대비 80% 이하
3. **카테고리 격리**: LLM 프롬프트만으론 불가능, 후처리 자동 교정 필수
4. **PowerShell `Invoke-RestMethod`**: 한글 깨짐, Swagger UI나 Python으로 우회
5. **네트워크 드라이브 venv**: PC 종속이라 동기화 안 됨, PC마다 별도 생성
6. **Streamlit 버튼 클릭**: `st.columns` 안에서 `st.rerun()` 호출 시 클릭 신호 소실 → **`on_click` 콜백 방식 사용**
7. **Streamlit text_input**: 실시간 갱신 안 됨 (blur 시점에만 서버 전달)

### 다음 단계 시작 전 확인 사항
- [ ] 페이즈 3 작업: 이력 페이지, 엑셀 출력
- [ ] 사장님 결정: 4단계 진입 시 비전 모델(llama3.2-vision) 통합 방식
- [ ] qwen3.6:27b, qwen3.6:35b-a3b 삭제 여부 (디스크 40GB 확보 가능)

### 매 세션 시작 시 확인
```powershell
# 1. Z 드라이브 매핑 확인
dir Z:\

# 2. 서버 살아있는지 확인
start http://192.168.0.200:8000/docs

# 3. GUI 실행
# (E:\성인용품 등록 반자동화\ 폴더에서)
.\run_gui.bat
```
