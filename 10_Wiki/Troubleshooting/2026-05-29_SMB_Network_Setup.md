---
id: 53a29881-2244-4f24-91bf-a841ec2912af
aliases: [SMB 네트워크 드라이브, 오류 86, 로컬 계정 우회, 2.5Gbps, 올라마 파일 공유]
category: "[[10_Wiki/Troubleshooting]]"
confidence_score: 0.95
tags: [SMB, 인프라설계, Ollama, 2.5Gbps, 트러블슈팅, 보안우회]
entities: [PER: 세현, ORG: Ollama, TECH: SMB, PowerShell]
last_reinforced: 2026-05-29
github_commit: ""
---

# [[2026-05-29 SMB 네트워크 드라이브(Z:) 구축 및 트러블슈팅]]

## 📌 한 줄 통찰 (Abstractive Summary)
> 마이크로소프트 계정 연동 및 Windows Hello 보안으로 인한 SMB 접근 권한 오류를 로컬 전용 계정 신설 방식으로 우회하여, 메인-세컨 PC 간 초고속 파일 공유 시스템을 구축함.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 보안 인증(온라인 계정)으로 인한 권한 충돌 시, 공유 전용 오프라인 로컬 계정을 신설하여 인증 레이어를 우회하는 네트워크 구축 패턴.
- **세부 내용:**
  - **구축 목표:** 메인 PC와 세컨 PC(올라마 서버) 간 2.5Gbps 내부망을 통한 Z: 드라이브 매핑. (목적: `adult_product_renamer` 소싱 자동화 연동)
  - **오류 증상:** 오류 86(네트워크 암호 불일치), 오류 8646(계정 권한 없음), 오류 67(네트워크 이름 미발견), 액세스 거부 등 다발적 권한 에러 발생.
  - **원인:** 세컨 PC가 MS 온라인 계정 연동 및 PIN 번호 사용 중이라, `net use` 방식의 암호 주입이나 `net user` 명령어를 통한 비밀번호 제어가 차단됨.
  - **해결책:** 세컨 PC에 공유 전용 로컬 계정(`sehyun`)을 `net user sehyun 138074 /add` 로 신설하고, NTFS 시스템의 보안 탭(ACL)에서 해당 계정의 읽기/쓰기 권한을 부여함.

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 복잡한 MS 보안 인증을 정면 돌파하지 않고 전용 로컬 계정을 신설해 우회(Bypass)한 점은 매우 실용적인 인프라 구축 사례입니다. 향후 다른 PC 자원이나 NAS 등을 연결할 때도, '공유 전용 로컬 계정'이라는 독립된 자격 증명을 활용하면 보안과 접근성을 모두 챙길 수 있는 강력한 인프라 템플릿이 될 것입니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 연결:** 내부망 연결 시 항상 IP와 계정명(ID) 불일치 여부를 최우선으로 검증해야 함을 재확인.
- **정책 변화:** 인프라 통신 아키텍처(Ollama 포트 제어 + SMB 파일 공유)를 분리하여 제어하는 인프라 설계 지식 가중치 상향 🧠

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/Troubleshooting]]
- **Related:** [[시스템_자동화_및_파이프라인]], [[Ollama_인프라]]
- **Raw Source:** [[99_Archive/Raw_Backup/2026-05-29_gemini-code-1780046319325.md]]
