# CASE STUDY — 누끼 GPU(세컨 PC) 이전 시도 → 메인 로컬 회귀

> 문서 성격: 검증 케이스 스터디. "실패도 경험" — 세컨 PC GPU로 누끼를 옮겼다가
> VRAM 한계와 작업 패턴 분석 끝에 메인 로컬로 되돌린 전 과정.
> 기술은 성공(GPU 누끼 10배 빠름), 그러나 사장님 작업 패턴에선 이득 없음을 확인.
> 코드는 보존(플래그 OFF) — 작업 방식 바뀌면 재활용.
>
> 작성: 2026-06-02 / 세현 사장님 / 항상 존댓말
> 관련: REF_GPU_CUDA_FIX.md(GPU DLL 해결), PHASE2_FASTAPI(상품명 서버)

---

## 0. 한 줄 결론

누끼(rembg+BiRefNet)를 세컨 PC RTX 5060으로 옮겨 **순수 속도는 9~15초→1~2초(10배)**
달성. 그러나 VRAM 16GB에 qwen3(14GB)+누끼(8GB) 동시 적재 불가 →
**누끼/상품명 전환마다 8~9초**(qwen3 언로드). 사장님 작업이 "상품명+누끼 하나씩"
번갈아라 전환비용이 GPU 이득을 다 먹음 → 메인 CPU와 사실상 동급.
**결정: 누끼는 메인 로컬 CPU로 회귀(CUTOUT_REMOTE=False). 원격 코드는 보존.**

---

## 1. 동기 / 가설

- 메인 PC 누끼가 CPU(RX570은 CUDA 불가)로 9~15초 → 느림.
- 세컨 PC RTX 5060(16GB)이 상품명(qwen3)만 쓰고 GPU 여유 있어 보임.
- 가설: 누끼도 세컨 GPU로 보내면(FastAPI /cutout) 1초 미만 + 메인 부담↓.
- 2.5G 내부망 + Z: 공유라 전송도 빠를 것으로 기대.

---

## 2. 진행 단계 (전부 기술적으로는 성공)

### 2-1. 세컨 PC 누끼 환경 점검
- 누끼 방식 = rembg + BiRefNet-general (onnxruntime). ~/.u2net/birefnet-general.onnx(927MB).
- GPU 막힘: onnxruntime-gpu 1.26이 요구하는 CUDA12 런타임 중 cudart64_12.dll 누락.
  · cublas/cudnn은 있는데 cudart64_12.dll만 빠짐 → CPU 폴백.

### 2-2. GPU 살리기 (REF_GPU_CUDA_FIX 갱신)
- nvidia pip 휠 보충: nvidia-cuda-runtime-cu12==12.9.79, cufft/curand/cusparse-cu12(+nvjitlink). venv 안에만.
- ★ 결정적 발견: `os.add_dll_directory`만으로 onnxruntime이 못 찾음 → **PATH prepend가 핵심**.
- gui/gpu_dll.py(register_cuda_dlls) 신규 + rembg import 전 호출.
- 시스템 CUDA 13.2 / Ollama 안 건드림.
- 결과: CUDAExecutionProvider 작동(GPU 91%), CPU 폴백 아님 확정. 누끼 0.6~1초.

### 2-3. FastAPI 안정화 (/cutout은 이미 존재)
- /cutout 엔드포인트는 페이즈 4-3b에 이미 있었음(process_image 호출).
- 콜드 84초(첫 추론 cuDNN 캐시 빌드) → lifespan 워밍업으로 기동 시점 이동.
- 입력: image_path(경로) 또는 image_base64. 출력: cutout_path(투명 누끼),
  thumbnail_path, (옵션)thumbnail_base64. ★투명 누끼는 경로로만(base64 없음).

### 2-4. 메인 PC 연결 (경로 방식, 본인 환경 전용)
- 입출력 다 경로(3번): 본인 환경 Z: 있으니 base64 인코딩 불필요, 가장 간단.
- 경로 변환 헬퍼(메인 Z: ↔ 세컨 C:\Users\pthem\...), 왕복 검증.
- make_cutout 반환 타입 그대로 → _make_thumbnails 무수정.
- CUTOUT_REMOTE 플래그 + 로컬 CPU 폴백(세컨 꺼져도 작업 안 끊김).

---

## 3. 🔴 실제 측정에서 드러난 진실 (사장님 의심이 정확)

### 3-1. 깨끗한 서버 로그 측정값
```
누끼 연속:        8.9초(첫,세션재생성) → 2.0초 → 1.5초  (점점 빨라짐)
상품명(/rename):  10초 (누끼 세션 해제 → qwen3 적재)
상품명 직후 누끼:  8.7초 (qwen3 언로드 8초 + 누끼 1초)  ← 전환비용 부활
```
- 매 /cutout 로그에 "qwen3 언로드 요청(keep_alive=0)" 찍힘.
- 매 /rename 로그에 "누끼 세션 해제 — qwen3에 VRAM 양보" 찍힘.

### 3-2. 근본 원인 = VRAM 16GB 부족 (수학적 공존 불가)
```
qwen3:14b @ ctx 32768 = 14.3GB (keep_alive로 idle에도 상주)
BiRefNet 누끼 1장      = ~7.6GB
합계 ~22GB ≫ 16GB
qwen3 4k로 줄여도 9.9+7.6=17.5GB → 여전히 초과
```
→ 한 번에 한 엔진만 GPU에 둘 수 있음 → 상호 축출 → 전환마다 8~9초.

### 3-3. 사장님 작업 패턴과의 충돌
- 작업 = "한 번에 하나의 아이템 수동"(상품명+누끼 한 세트씩 번갈아).
- → 누끼할 때마다 직전에 상품명 썼으니 매번 qwen3 언로드 8초.
- 세컨 GPU 누끼(1초) + 전환(8초) + Z: 전송 ≈ 9초+ ≈ 메인 CPU(9~15초).
- **GPU의 이득이 전환비용에 전부 잠식됨.**

### 3-4. 함정도 하나 — start로 띄운 서버
- 서버켜기.bat이 `start`로 띄워 cmd창 ≠ 서버프로세스.
- cmd 닫아도 구버전 서버가 8000 점유 → 새 서버 bind 실패(WinError 10048).
- "서버 껐는데 빨라짐" 착각의 원인 = 어느 서버가 도는지 뒤죽박죽이었음.
- 교훈: 측정 전 `netstat -ano | findstr :8000` + `taskkill`로 포트 정리.

---

## 4. 품질 확인 (사장님 질문)

- 메인/세컨 둘 다 **같은 birefnet-general** 모델 + 같은 1500px 전처리.
- → 누끼 품질 동일. CPU/GPU는 속도만 다르고 품질 무관.
- 미세 차이 가능성: 부동소수점(육안 구분 불가), 전처리 크기(양쪽 1500px 동일이면 OK).
- 결론: 품질 이유로 GPU를 고집할 필요 없음. → 로컬 회귀에 품질 손실 없음.

---

## 5. 결정 — 메인 로컬 CPU로 회귀

- `CUTOUT_REMOTE = False` → make_cutout이 항상 로컬 CPU(birefnet-general).
- 이유: ①품질 동일 ②사장님 패턴엔 세컨 GPU 이득 없음(전환 8초) ③단순함.
- 원격 코드(api_client.cutout, 경로변환, cutout_io, gpu_dll)는 **지우지 않고 플래그로만 OFF**.
  · 재활용 조건: 누끼를 "배치"로 몰아서 할 때 → True로 켜면 1~2초씩(전환 1회뿐).
- 세컨 PC 서버(qwen3 /rename 상품명)는 **계속 사용**. 누끼(/cutout)만 메인이 안 부름.

---

## 6. 세컨 GPU가 "빛나는" 조건 (미래 재활용 지침)

```
[이득 없음 — 현재]  상품명↔누끼 번갈아 하나씩  → 전환 8초마다 → 메인 CPU와 동급
[이득 큼 — 미래]    누끼만 몰아서 연속(배치)    → 전환 1회 → 1~2초씩 → 10배 빠름
[이득 큼 — 대안]    상품명을 클라우드 API로 분리 → 세컨 GPU 누끼 전용 → 항상 1~2초
```
→ 작업 방식이 배치로 바뀌거나, 상품명을 qwen3 대신 클라우드(Claude/ChatGPT 구독)로
  빼면 그때 CUTOUT_REMOTE=True 재활성화 검토.

---

## 7. 새 결정 기록 (DECISIONS.md, D-067~)

- D-067: 누끼는 메인 로컬 CPU(CUTOUT_REMOTE=False). 품질은 세컨 GPU와 동일(같은
  birefnet-general)이고, 사장님 패턴(상품명+누끼 하나씩)에선 VRAM 부족발 전환비용
  8초가 GPU 이득을 잠식 → 로컬이 더 단순하고 동급. 원격 코드는 보존.
- D-068: 세컨 PC GPU 누끼 자체는 성공(0.6~1초). 막힘 원인 cudart64_12.dll 누락 →
  nvidia pip 휠 + PATH prepend로 해결(os.add_dll_directory만으론 부족). REF_GPU_CUDA_FIX 갱신.
- D-069: VRAM 16GB엔 qwen3(14GB)+BiRefNet(8GB) 동시 적재 불가 → 시간분할(상호축출)로만
  공존. 전환비용 8~9초. 누끼 몰아치기(배치) 또는 상품명 클라우드 분리 시 GPU 재활용 가능.

---

## 8. 교훈

1. **빠른 부품 ≠ 빠른 작업**: 누끼 1초여도 전환 8초면 작업은 9초. 부품 속도가 아니라
   "작업 패턴 위에서의 총 시간"으로 판단해야 한다.
2. **VRAM은 수학**: 모델 크기 합이 VRAM 넘으면 공존 불가. 직렬화·다운스케일로도 못 줄임
   (arena가 상주 footprint를 다 잡음). 합산부터 해본다.
3. **작업 패턴을 먼저 묻는다**: 배치냐 인터리브냐로 GPU 이득이 정반대. 최적화 전에
   사용자 워크플로를 확정.
4. **측정 전 환경 정리**: start로 띄운 좀비 서버가 포트 점유 → 측정 오염. netstat+taskkill로
   깨끗이 한 뒤 측정.
5. **품질과 속도 분리해 본다**: 같은 모델이면 CPU/GPU 품질 동일. 속도 때문에 품질 걱정할 필요 없음.
6. **되돌릴 수 있게 만든다**: CUTOUT_REMOTE 플래그 덕에 회귀가 1줄. 실험적 기능은
   플래그로 분리해 지우지 않고 끄기 → 재활용 가능. "실패도 경험"을 자산으로 남김.
7. **GPU DLL 함정**: onnxruntime-gpu는 자기용 CUDA12 런타임 휠 필요(시스템 CUDA와 별개).
   os.add_dll_directory만으론 부족, PATH prepend 필요.

---

## 9. 함정 추가 (RUNBOOK 보강, 44~)

44. 세컨 GPU에 LLM(qwen3 14GB)과 누끼(8GB) 둘 다 두면 VRAM 16GB 초과 → 상호 축출
    전환비용 8~9초. 인터리브 작업이면 GPU 이득 사라짐. 배치/분리 시에만 이득.
45. FastAPI를 start로 띄우면 cmd 닫아도 서버 상주 → 재실행 시 포트 충돌(10048).
    측정/재시작 전 netstat -ano|findstr :8000 + taskkill로 정리.
46. onnxruntime-gpu = 자기용 CUDA12 런타임 휠 필요(cudart64_12.dll 등). 누락 시 조용히
    CPU 폴백. PATH prepend로 DLL 노출(os.add_dll_directory만으론 못 찾음).
47. CPU/GPU 누끼 품질은 같은 모델이면 동일. 속도만 차이.
48. 실험 기능은 플래그(CUTOUT_REMOTE)로 분리 → 회귀 1줄, 코드 보존해 재활용.

---

*문서 끝. 핵심: 기술 성공·작업이득 없음 → 로컬 회귀, 코드는 플래그로 보존(재활용).
실패가 아니라 "VRAM 한계와 작업패턴의 관계"를 직접 확인한 값진 검증.*
