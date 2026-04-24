---
id: YEGOMCAPTURE-DEV-HISTORY-1.0
aliases: [YegomCapture 개발 히스토리, 예곰 캡쳐, 화면 캡쳐 프로그램]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 1.0
tags: [project, yegomcapture, python, automation, deployment, troubleshooting]
last_reinforced: 2026-04-24
github_commit: "1b928e7"
---

# [[YegomCapture 개발 히스토리]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> YegomCapture(예곰 캡쳐)의 신규 그리기 기능 추가, 업데이트 무시 로직 적용, 그리고 GitHub 릴리즈 배포 파이프라인 및 랜딩페이지 통합 자동화에 대한 개발/인프라 통합 기록.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 사용자 편의성 증대(그리기 기능 및 업데이트 알림 제어), 배포 스크립트 정규식 고도화(단일 스크립트로 다운로드 링크와 홍보 뱃지 동시 치환), 사용자 가이드 직관성 강화(권한 에러 방지).
- **세부 내용:**
  1. **코어 로직 & 신규 기능 (유부장):**
     - 캡쳐된 이미지 미리보기 창에 마우스 드래그로 빨간색 사각형을 그려 저장할 수 있는 편집 기능 추가.
     - 시작 시 노출되는 '업데이트 알림' 팝업에 "현재 버전에 대한 알림 다시 보지 않기" 체크박스 추가. `config.json`의 `ignored_update_version`에 기록하여 동일 버전 알림 무시 (신규 버전은 정상 알림).
  2. **릴리즈 파이프라인 & 랜딩페이지 최적화 (이과장):**
     - `scripts/bump_and_release.py` 정규식 로직을 수정하여 버전업 시 `index.html` 내 다운로드 링크 파일명이 갱신되지 않는 404 에러 픽스.
     - 랜딩페이지 상단 홍보용 버전 뱃지(예: `V1.0.4 업데이트`) 텍스트도 자동 치환하도록 정규식 연동 완료.
     - `index.html` 및 `guide.html`에 "setup.exe를 관리자 권한으로 실행" 문구 추가하여 권한 에러 방지.
  3. **문서화 및 로직 감독 (박상무):**
     - 각 에이전트의 작업 내역 종합 및 문서화 (유지보수용 레퍼런스 확립).

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 기존 배포 스크립트는 다운로드 링크만 치환하거나 이전 버전에 멈춰 있어 404 에러를 유발. 
- **정책 변화:** 신규 기능 배포 시 랜딩페이지 홍보 텍스트와 릴리즈 스크립트의 정규식 매칭을 상호 크로스체크(유부장 ↔ 이과장)하는 프로세스를 에이전트 SKILL에 업데이트함 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects]]
- **Related:** [[Lee-Gwajang_Deployment_Pipeline]], [[Python_Automation]]
- **Raw Source:** `[[00_Raw/yegomcapturefix.md]]`
