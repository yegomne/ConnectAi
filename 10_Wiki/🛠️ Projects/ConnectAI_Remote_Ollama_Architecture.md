---
id: c7f3a8b4-92e1-4c7a-bb2a-9e3d9f123456
aliases: [Connect AI Ollama, 원격 LLM 연결, 포트프록시 설정, CSP 우회]
category: "[[10_Wiki/🛠️ Projects]]"
confidence_score: 0.95
tags: [ConnectAI, Ollama, Portproxy, Firewall, Architecture, CSP]
entities: [TECH: Connect AI, TECH: Ollama, TECH: Antigravity, ORG: Windows portproxy, TECH: Windows Defender 방화벽, TECH: CSP]
last_reinforced: 2026-05-11
github_commit: "TBD"
---

# [[ConnectAI_Remote_Ollama_Architecture]]

## 📌 한 줄 통찰 (Abstractive Summary)
> Antigravity의 CSP 제한을 우회하기 위해 Windows portproxy를 브릿지로 활용하여, 로컬 환경(127.0.0.1:11434)에서 원격 LLM 서버(192.168.0.200:11434)의 Ollama 모델들을 안전하게 호출하는 투명한 연결망을 구축하다.

## 📖 구조화된 지식 (Synthesized Content)
- **추출된 패턴:** 로컬 전용 보안 정책(CSP)으로 인해 LAN IP 접근이 차단될 경우, 로컬 루프백(127.0.0.1)으로 포트를 포워딩(portproxy)하여 시스템 내부망과 외부망을 중계하는 패턴.
- **세부 내용:**
  - **아키텍처 흐름:** `Antigravity (Connect AI) → 127.0.0.1:11434 → Windows portproxy → 192.168.0.200:11434 (LLM 컴퓨터) → Ollama 모델`
  - **프록시 설정:** 관리자 권한 CMD에서 `netsh interface portproxy add v4tov4 listenaddress=127.0.0.1 listenport=11434 connectaddress=192.168.0.200 connectport=11434` 실행.
  - **CSP 우회:** Antigravity Webview는 `http://192.168.0.200:11434`를 차단하지만 `http://127.0.0.1:11434`는 허용하므로, Connect AI 설정 JSON(`connectAiLab.ollamaUrl`)에 후자를 입력하여 회피.
  - **보안/방화벽 통제:** 외부 침입을 막기 위해 LLM 컴퓨터의 Windows Defender 방화벽 인바운드 규칙(11434 포트)에서 **원격 IP를 Antigravity 컴퓨터의 실제 IP 단 하나로만 제한** (공유기 포트포워딩, DMZ 절대 금지).
  - **설치 모델 라인업 및 운영 기준:** 
    - `deepseek-coder-v2:16b` : 일반 코딩, 에러 분석 (기본 메인 모델)
    - `qwen3-coder:30b` : 복잡한 설계, 다파일 리팩토링 (고난도 작업용)
    - `gemma4:e4b` : 빠른 요약, 메모, 가벼운 질문 (속도 우선)
    - `llama3.2-vision:latest` : 이미지, 스크린샷 화면 분석

## 💎 대체 불가능한 가치 (Unique Value & Expansion)
- 단순히 로컬에서 모델을 띄우는 한계를 넘어, **고사양 연산을 전담하는 외부 LLM 서버를 투명하게 통합**함으로써 Antigravity 환경의 작업 효율을 극대화했습니다. 
- 이 구조는 향후 다른 멀티 에이전트(예: 김대리, 유부장 등)가 각기 다른 무거운 모델(비전, 코드 전용 등)을 동시다발적으로 호출할 때에도 메인 PC의 리소스 부담을 없애주는 '분산 AI 컴퓨팅'의 초석이 될 것입니다.

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **보안 정책 업데이트:** 과거 "모든 IP 허용" 등 느슨했던 로컬망 연결 방식을 탈피하고, 방화벽 단에서 "특정 IP(Antigravity 컴퓨터) 단일 허용"을 규칙화하여 공용 네트워크에서도 안전한 Private AI API 서버망을 구성했습니다. IP 변동에 따른 단절 리스크를 막기 위한 라우터(공유기) 단의 고정 IP 할당(DHCP) 중요성도 새롭게 추가되었습니다.

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/🛠️ Projects]]
- **Related:** [[Antigravity_Architecture]], [[Local_LLM_Optimization]]
- **Raw Source:** [[00_Raw/2026-05-11/Ollama_Connection_Log]]
