---
id: TASKJELLY-SOUND-1.0
aliases: [TaskJelly 사운드 트러블슈팅, DOMException 오디오 에러, 파이썬 오디오 합성]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 1.0
tags: [project, taskjelly, audio, troubleshooting, python, wav, DOMException]
last_reinforced: 2026-04-22
github_commit: "2f3f018"
---

# [[TaskJelly 사운드 트러블슈팅 (DOMException 및 파이썬 파형 합성)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> 외부 오디오 에셋(MP3)의 404 차단으로 인한 브라우저 `DOMException` 에러를, 파이썬 기반 순수 `.wav` 파형 합성 및 에러 핸들링 파이프라인으로 완벽하게 해결한 트러블슈팅 기록.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 외부 에셋 의존성 최소화(Zero-Dependency Audio), 오디오 파일 무결성 검증, 비동기 브라우저 오디오 재생 타이밍 동기화 패턴.
- **세부 내용:**
  1. **이슈 발생 원인 (`DOMException`):** 외부 서버(OpenGameArt) 보안 정책으로 인해 다운로드한 `.mp3` 파일이 실제로는 404 HTML 문서로 저장됨. 브라우저의 `new Audio().play()`가 이를 디코딩하지 못하고 `DOMException (NotSupportedError)`을 발생시키며 사운드 출력이 무력화됨.
  2. **오디오 파형 직접 합성 (Python):** 외부 링크 에러를 원천 차단하기 위해 파이썬 `math.sin` 파형 계산을 통해 주파수 대역을 직접 깎아 `.wav` 파일 생성.
     - `slot-spin.wav`: 400Hz 대역 기준 긴장감 넘치는 요동치는 파형.
     - `slot-win.wav`: C5, E5, G5 코드를 활용한 승리감 팡파레 파형.
  3. **타이밍 동기화 (Timeouts):** 슬롯머신 로직의 3초 딜레이(`setTimeout`)에 맞춰 사운드 객체 로드 및 재생 타이밍을 동기화하여 완벽한 타격감 확보.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 무분별한 외부 리소스 링크 사용은 서비스 안정성(오디오 객체 파괴)에 치명타를 줄 수 있음을 깨달음.
- **정책 변화:** 
  1. **음원 파일 무결성 검증:** 파일의 확장자만 신뢰하지 않고, 용량(Bytes) 및 헤더 정보를 검증하는 단계를 오디오 파이프라인 정책에 추가 🧠.
  2. **오디오 에러 핸들링 강화:** `.play().catch(...)` 구간에 명시적 fallback(기본 비프음 등) 로직을 추가하여 무음 상태를 방지하는 강건한 아키텍처로 업데이트 🧠.

## 🔗 지식 연결 (Graph)
- **Parent:** [[TaskJelly_Project]]
- **Related:** [[Zero_Dependency_Architecture]], [[Browser_Audio_API]]
- **Raw Source:** `[[00_Raw/TaskJelly_soundfix.md]]`
