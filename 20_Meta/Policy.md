# 🧠 P-Reinforce RL Policy & Weights

## 📊 Current Weights
- `w1` (Categorization Accuracy): 1.0
- `w2` (Graph Connectivity): 1.0
- `w3` (User Satisfaction): 1.0

## 🚦 Classification Boundaries
- **Projects**: 진행 중이거나 구체적인 목표가 있는 업무.
- **Topics**: 개발, 마케팅, 심리학 등 보편적/영구적 개념.
- **Decisions**: 판단, 아키텍처 선택, 전략적 의사결정 기록.
- **Skills**: 즉시 적용 가능한 프롬프트, 도구 사용법, 자동화 파이프라인.

## 💡 Learned Preferences
- **Image Fallback Policy (할루시네이션 및 이미지 깨짐 방지):**
  - 답변 첫 줄에 아위키의 표정(이미지)을 출력할 때, `SKILL.md`에 정의된 12개의 공식 이미지 링크 이외의 파일명을 임의로 생성(Hallucination)하는 것을 엄격히 금지합니다.
  - 확신이 서지 않거나 맞는 이미지가 없을 경우, 엑스박스(깨진 이미지) 출력을 원천 차단하기 위해 무조건 본인의 `SKILL.md` 에 정의된 공식 이미지 링크를 직접 조회하여 대체 이미지로 Fallback 처리합니다.
- **Language & Encoding Policy (타협안 적용):**
  - **시스템 뼈대 (System Structure):** 디렉토리 경로, 폴더명, 파일명, 파일 ID 등 물리적인 인프라 명칭은 OS 간 인코딩 충돌 및 터미널 에러를 차단하기 위해 무조건 **영어(English)**를 유지합니다.
  - **지식 및 보고서 (Content & Report):** 하지만 마크다운 내부 본문(제목, 내용), 옵시디언 Aliases, 그리고 A-Wiki가 직접 보고하는 작업 보고서는 대표님의 완벽한 가독성을 위해 100% **한글(Korean)**로 번역/표기하여 제공합니다.
- **작업 지시어 기반 자동 파이프라인 (Trigger Protocol):**
  - 대표님이 00_Raw 폴더의 `.md` 파일을 전달하며 **"작업해"** 또는 **"작업해줘"**라고 지시할 경우, 추가 설명이 없더라도 묻지도 따지지도 않고 즉시 `📝 지식 문서 변환 규격(The Wiki Template)`을 적용하여 구조화 작업을 진행하며, 최종 보고는 반드시 A-Wiki 표준 답변 포맷과 마크다운 코드 블록으로 출력해야 합니다.
  - 대표님이 **"퇴근"**이라고 말씀하실 경우, 그날 `00_Raw/sehyun.md` (대표님 생각 보관소)에 쌓인 타임라인 기록들을 자동으로 분석하여 정식 지식 문서(`10_Wiki/`)로 분류 및 구조화(지식망 연결) 작업을 수행하고, 로컬 커밋과 원격 GitHub Push 동기화를 일괄 진행합니다.
- **Identity Separation Policy (정체성 분리 정책):**
  - **Yegom (예곰):** 기업(Company), 비즈니스, 1인 창업가 브랜드로서의 시스템 아키텍처 및 업무 지식과 관련된 영역입니다.
  - **Sehyun (세현):** 대표님의 자연인(개인), 고유 자아, 감정 일기, 가족사 및 지극히 사적인 라이프 로깅 영역입니다. 개인적인 기록은 모두 `sehyun` 계열의 파일명과 카테고리(`10_Wiki/👤 Sehyun/`)를 명시적으로 사용하여 비즈니스 데이터와 영구히 분리합니다. 
    - **피드백 반영 (Boundary Shift):** 일상/일기(Diary)에서 파생된 콘텐츠(예: 쇼츠 대본 등)라 할지라도, 그 뿌리가 되는 개인적 경험과 감정선이 메인이라면 `10_Wiki/💡 Topics/Content_Ideas`가 아닌 `10_Wiki/👤 Sehyun/Diary`에 우선적으로 분류 및 영속화합니다.
    - **자동 파생 파이프라인 (Diary to Shorts):** 일기/일상(Diary) 데이터를 제공받을 경우, 단순 요약으로 끝내지 않고 지식 구조화 단계에서 반드시 **'대체 불가능한 가치 (Unique Value & Expansion)' 섹션에 숏폼(Shorts) 3부작 대본 초안**을 파생 콘텐츠로 기획하여 포함시킵니다. (Visual, Voice, BGM/윤사원 호출 등 시청각 기획 요소 필수 포함)
- **Data Integrity & Backup Policy (데이터 무결성 및 백업 정책):**
  - **직관적 백업 네이밍 (Title-based Archiving):** `temp/` 폴더에서 `99_Archive/Raw_Backup/`으로 원본을 백업할 때, 파일 충돌 방지와 인간의 직관적인 가독성을 동시에 만족시키기 위해 본문 첫 줄의 `# 제목(H1)`을 파싱하여 파일명 접두사로 사용합니다. (예: `실행매뉴얼_RUNBOOK_YYYYMMDD_HHMMSS.md` 또는 서브 폴더 격리) 
  - **작업 완료 표식 (Processed Marking Policy):** 대표님이 직관적으로 '지식화 구조화 완료' 여부를 파악하실 수 있도록, 백업되는 모든 원본 파일의 파일명 최상단(앞부분)에 반드시 **`[AWIKI_DONE]_`** 이라는 명확한 표식을 붙여서 아카이빙합니다.
  - **블랙리스트 격리:** `99_Archive/` 내의 파일들은 RAG 검색 및 지식 병합 연산에서 완벽하게 제외되어 원본 훼손 및 오염을 차단합니다.
