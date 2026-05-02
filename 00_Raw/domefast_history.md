# Domefast (도매매 소싱 대시보드 & 자동화 앱) 작업 히스토리

## 프로젝트 개요
도매매(도매꾹) 사이트의 상품 URL 또는 엑셀 리스트를 입력받아, 백그라운드에서 크롤링, 이미지 배경 제거(rembg), 구글 Gemini AI 기반 상품명 최적화 및 쿠팡 태그 추출을 원클릭으로 자동화하는 시스템. (데스크톱 네이티브 앱 + 다운로드용 웹 랜딩페이지)

## 🕒 최근 작업 내역 (2026-05-02)

### 1. 다운로드 링크 및 2FA 에러 해결
- **문제:** 웹 랜딩페이지(`page.tsx`)의 다운로드 버튼이 존재하지 않는 프라이빗 저장소(`domeggook-tool`)를 가리켜 다운로드 시 404 및 2FA 인증 에러가 발생함.
- **해결:** `downloadLink`를 실제 퍼블릭 저장소인 `https://github.com/yegomne/domefast-web/releases/download/v1.0.0/domeggook_tool.exe`로 변경하고 Vercel에 자동 배포. GitHub Release에 `.exe` 파일을 정상 업로드 완료.

### 2. 브랜딩 및 디자인 에셋 고도화 (김대리)
- **작업 내용:** 배경이 투명한 3D 스타일의 고품질 로고(`app_icon.png`, `app_icon.ico`) 생성 및 적용.
- **적용처:** 데스크톱 앱 실행 아이콘 및 상단 로고, 웹 대시보드 Favicon 일괄 적용.

### 3. 엑셀 대량 처리 (Batch Processing) 파이프라인 구축 (유부장)
- **UI 업데이트:** `main_desktop.py`에 '엑셀 대량 자동화 (Batch)' 모드 라디오 버튼 및 `.xlsx` 파일 선택기 추가.
- **스마트 컬럼 인식:** 엑셀의 특정 열 위치에 의존하지 않고, 헤더에서 `'자체상품코드'` 텍스트를 검색하여 해당 열의 데이터를 자동으로 긁어오도록 구현.
- **무중단 릴레이 (Queue):** `BatchManager` 클래스를 도입하여 여러 상품을 순차적으로 처리. 중간에 에러(이미지 없음, 통신 실패 등)가 발생해도 프로그램이 멈추지 않고 에러 로그만 기록한 채 다음 상품으로 넘어감.
- **진행 상태 UI 표시:** Progress Bar 및 텍스트를 통해 현재 처리 현황(예: `[Batch] 3/20 진행 중...`)을 직관적으로 표시.
- **결과 추출:** 배치 처리가 모두 끝나면 취합된 데이터를 `pandas`를 이용해 `결과_엑셀파일.xlsx`로 일괄 내보내기 구현.

### 4. API Rate Limit (429) 방어 로직 추가
- **문제:** 무료 티어 Gemini API 사용 시 분당 요청 수 제한(RPM) 초과로 인한 에러(`429 You exceeded your current quota`) 발생.
- **해결:** `worker.py`의 `OptimizeWorker`에 429 에러 발생 시 프로그램 종료를 막고 자동으로 **60초 대기 후 재시도(최대 3회)**하는 불굴의 쉴드 로직(Retry mechanism) 추가.

## 🚀 향후 과제 (To-Do)
- 수정된 `main_desktop.py`, `worker.py` 및 신규 아이콘이 반영된 최종 버전의 `domeggook_tool.exe` PyInstaller 재빌드 및 GitHub Release 덮어쓰기.
- 실제 도매매 대량 엑셀 데이터를 바탕으로 장시간 동작 시 메모리 누수 여부 모니터링.
