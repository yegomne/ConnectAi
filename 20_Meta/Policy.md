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
