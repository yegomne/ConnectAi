---
id: d8d3c59a-14d1-419b-b0b2-4d2a1b1837f4
aliases: [도매패스트, Domefast, 도매꾹 자동화, 도매매 소싱 대시보드]
category: "[[10_Wiki/🛠️ Projects/Domefast_Development_History]]"
confidence_score: 1.0
tags: [자동화, 크롤링, AI소싱, 쿠팡, 배치처리]
entities: [TECH: Domefast, TECH: Gemini AI, TECH: rembg, TECH: Vercel, TECH: PyInstaller, ORG: 도매꾹]
last_reinforced: 2026-05-02
github_commit: ""
---

# [[Domefast 개발 히스토리 (Domefast Development History)]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 도매매 상품 소싱의 모든 과정(크롤링, 배경 제거, AI 상품명/태그 최적화)을 원클릭 및 대량 엑셀 처리(Batch)로 자동화하여, 쇼핑몰 운영자의 시간을 극적으로 압축하고 API 통신 안정성을 확보한 'Domefast' 프로젝트의 핵심 이정표입니다.

## 📖 구조화된 지식 (Synthesized Content)
- **프로젝트 개요:**
  - **핵심 기능:** 도매매(도매꾹) 사이트 상품 URL 또는 엑셀 리스트 입력 시 → 백그라운드 크롤링 → `rembg` 기반 이미지 배경 제거 → Gemini AI 기반 상품명 최적화 및 쿠팡 검색 태그 자동 추출.
  - **플랫폼 구조:** 데스크톱 네이티브 앱 (PyInstaller 빌드) + 배포용 웹 랜딩페이지 (Vercel 호스팅)
- **최신 마일스톤 및 문제 해결 (2026-05-02):**
  - **인프라 및 배포 정상화:** 웹 랜딩페이지 다운로드 시 발생하던 404/2FA 에러를 해결하기 위해, 프라이빗 저장소 링크를 실제 퍼블릭 릴리즈 경로(`domeggook_tool.exe`)로 변경 후 Vercel에 자동 배포 완료.
  - **디자인/브랜딩 고도화:** 투명한 3D 스타일의 고품질 로고 에셋(`app_icon.png`, `.ico`)을 생성하여 네이티브 앱 아이콘 및 대시보드 Favicon에 일괄 적용 (시각적 퀄리티 상승).
  - **엑셀 대량 처리(Batch) 파이프라인 구축:** 
    - `main_desktop.py` 내 엑셀 선택 UI 및 스마트 컬럼('자체상품코드') 헤더 자동 인식 기능 추가.
    - `BatchManager` 클래스를 도입하여 에러(이미지 없음, 통신 실패 등) 시에도 중단 없이 로그만 남기고 릴레이 처리하는 무중단 큐(Queue) 완성.
    - 실시간 Progress Bar 진행률 노출 및 최종 완료 시 `pandas`를 이용한 결과 엑셀 일괄 내보내기 구현.
  - **API Rate Limit 방어 로직:** 무료 티어 Gemini API 사용 시 발생하는 429(Quota 초과) 에러 방지를 위해, `worker.py`에 에러 시 강제 종료를 막고 60초 대기 후 자동 재시도(최대 3회)하는 불굴의 쉴드(Retry) 로직 탑재.
- **🚀 향후 과제 (To-Do):**
  - 신규 로직 및 디자인이 반영된 최종 버전(`domeggook_tool.exe`)의 PyInstaller 재빌드 및 GitHub Release 덮어쓰기.
  - 대량 엑셀 데이터 장시간 동작 시 메모리 누수(Memory Leak) 모니터링.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 단순한 반복 수작업이었던 상품 리스팅 소싱 과정을 완전 자동화 시스템으로 치환함으로써, 대표님의 귀중한 시간과 인지 자원(Time-cost & Cognitive load)을 오프-로딩(Off-loading)하고 스케일업에 집중할 수 있게 되었습니다.
- 본 프로젝트에 적용된 `BatchManager`의 무중단 릴레이 기법과 429 에러 방어(Retry) 아키텍처는 향후 다른 자동화 파이프라인(예: TaskJelly 고도화 등)에 이식할 수 있는 매우 견고하고 범용적인 개발 자산이 됩니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 신규 생성된 문서입니다.
- **정책 변화:** 기존 수동 크롤링 방식에서 완전 무인화 대량 엑셀 처리(Batch Processing) 방식으로 패러다임이 진화하였으며, API 안정성을 최우선으로 하는 아키텍처 지침이 기록되었습니다.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects/Projects_Index]]
- **Related:** [[TaskJelly_Development_History]] (데스크톱 자동화 툴 및 UI 연동 패턴 공유)
- **Raw Source:** [[00_Raw/domefast_history.md]]
