# 참고: 세컨 PC GPU 살리기 (CUDA 13 vs onnxruntime CUDA 12 불일치 해결)

> 보관 목적: 데스크탑 전환(D-035) 후 누끼/검수를 세컨 PC GPU(RTX 5060 Ti)로
> 돌릴 때 다시 부딪힐 CUDA DLL 문제의 **검증된 해결책**을 보관한다.
> 지금은 적용 안 함(데스크탑 제작이 먼저). GPU 살릴 때 이 문서를 꺼낸다.
>
> 작성: 2026-05-30 / 출처: 사장님이 과거(도매패스트 엑셀 대량처리) 때 해결했던 방법 재확인

---

## 1. 문제 (이미 겪음)

```
세컨 PC: CUDA 13.2 설치됨
onnxruntime-gpu 1.26.0: CUDA 12 DLL(cublasLt64_12.dll) 요구
  → DLL 못 찾음 → GPU 로딩 실패 → CPU 폴백 → 135초 + 메모리 폭발 → 파섹 다운
```
- rembg의 엔진 = onnxruntime → 그래서 BiRefNet 누끼가 이 문제에 걸림.
- 과거 도매패스트 엑셀 대량처리 때도 같은 에러 → 아래 1번 방법으로 해결했었음(데자뷰).

## 2. 우리가 시도했다 실패한 것 (왜 실패했나)

```powershell
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12   # DLL은 설치됨
```
- DLL이 `venv\Lib\site-packages\nvidia\...\bin`에 깔렸지만,
  onnxruntime이 그 경로를 **PATH에서 못 찾아** 여전히 실패.
- → 빠진 조각 = **DLL 폴더 경로를 명시적으로 주입**하는 것. (아래 1번이 그걸 함)

---

## 3. 해결책 3가지 (1번 강력 추천)

### ⭐ 해결책 1: PyTorch lib 폴더의 DLL 경로 주입 (1순위)

PyTorch(CUDA 12 버전)는 자기 폴더(`torch/lib`)에 `cublasLt64_12.dll`을 이미 들고 있음.
onnxruntime이 그 폴더를 보게 만들면 DLL을 빌려 씀.

**스크립트 최상단(onnxruntime/rembg import 전)에 삽입:**
```python
import os
import torch  # torch 먼저 import (경로 확보용)

# PyTorch lib 폴더(cublasLt64_12.dll 등이 있는 곳)를 DLL 검색 경로에 주입
pytorch_lib_path = os.path.join(os.path.dirname(torch.__file__), "lib")
if os.path.exists(pytorch_lib_path):
    os.add_dll_directory(pytorch_lib_path)
    os.environ['PATH'] = pytorch_lib_path + ';' + os.environ.get('PATH', '')

import onnxruntime  # 이제 GPU 로딩 성공
# 이후 rembg new_session(...) 등 사용
```

**주의(원래 유부장 코드에서 보완한 점):**
- 원본은 `site.getsitepackages()[0]`를 썼는데 venv에선 인덱스가 빗나갈 수 있음.
- → `os.path.dirname(torch.__file__)`로 torch 위치를 직접 찾는 게 더 안전.

**전제 조건 (반드시 확인):**
```powershell
cd C:\Users\pthem\Documents\adult_product_renamer
.\venv\Scripts\activate
python -c "import torch; print('버전:', torch.__version__); print('CUDA:', torch.version.cuda); print('GPU인식:', torch.cuda.is_available())"
```
기대:
```
버전: 2.x.x+cu121 (또는 +cu124)   ← +cu12x 가 핵심
CUDA: 12.1 (또는 12.4)
GPU인식: True
```
- torch 없음 → `pip install torch --index-url https://download.pytorch.org/whl/cu121` (CUDA12 버전)
- torch가 +cpu 버전 → cublasLt64_12.dll 없음 → CUDA12 버전으로 재설치
- torch가 CUDA 13 버전 → cublasLt64_13.dll만 있어 또 불일치 가능 → CUDA12 버전 권장

### 해결책 2: 필요한 DLL만 스크립트 폴더에 복사 (단순/확실)
- CUDA 12.x 폴더나 공식 사이트에서 `cublas64_12.dll`, `cublasLt64_12.dll`, `cudnn64_8.dll` 등
  부족하다고 뜨는 파일만 복사 → 실행 스크립트(app.py/server.py)와 같은 폴더에 둠.
- 윈도우는 실행 파일과 같은 경로의 DLL을 최우선으로 읽음.
- 단점: DLL 출처 구해야 함, 버전 관리 지저분.

### 해결책 3: CUDA Toolkit 12.x 추가 설치 (정공법)
- 세컨 PC에 CUDA Toolkit 12.1(또는 12.4)을 **추가** 설치.
- 윈도우는 CUDA 여러 버전을 분리 관리 → 13.2 안 꼬임.
- onnxruntime-gpu가 C드라이브 CUDA 12 폴더를 찾아 DLL 물어옴.
- 단점: 수 GB 설치.

---

## 4. 데스크탑 전환과의 관계 (중요)

데스크탑(D-035)에서 누끼를 **어떤 방식으로 하느냐**에 따라 이 문제의 필요성이 갈림:

```
경우 A: 데스크탑에서도 rembg(onnxruntime) 사용
  → 위 1번 방법(PyTorch DLL 주입) 필요. 이 문서 그대로 적용.

경우 B: 데스크탑에서 PyTorch BiRefNet 직접 사용 (rembg 안 씀)
  → onnxruntime 자체를 안 쓰니 이 DLL 문제가 사라짐.
  → PyTorch가 CUDA를 알아서 관리 (Ollama처럼 깔끔). 더 권장될 수 있음.
```

**공통점: 둘 다 torch(CUDA 12)가 핵심.** 그래서 GPU 살릴 때 첫 단계는
"세컨 PC torch 상태 확인"(위 전제 조건 명령)이다.

---

## 5. GPU 살릴 때 진행 순서 (다음에 이거 보고 실행)

```
1. 세컨 PC torch 상태 확인 (3번 전제 조건 명령)
   ① +cu12x & True → 둘 다 가능
   ② +cpu → CUDA12 버전 재설치
   ③ 없음 → CUDA12 버전 설치
2. 방식 결정:
   - rembg 유지 → 해결책 1(DLL 주입) 적용
   - PyTorch BiRefNet 갈아타기 → onnxruntime 우회 (DLL 문제 없음)
3. 세컨 PC에서 누끼 테스트 → GPU로 1~3초 나오는지 확인
   (이전 CPU 9~15초 대비)
4. 메모리 모니터: nvidia-smi로 qwen3(9GB)+BiRefNet 공존 확인 (16GB 여유)
```

---

## 6. 관련 결정/맥락
- D-032: 세컨 PC GPU 시도 → CUDA 불일치로 무산, 일단 메인 PC CPU.
- D-035: 관제탑 데스크탑 전환.
- D-036: 데스크탑을 세컨 PC에서 실행하면 GPU 직접 활용 가능. CUDA는 이 문서로 해결.
- 전체 맥락은 `PHASE4_IMAGE_AND_DESKTOP_PIVOT.md` 참조.

---

*이 문서는 "나중에 GPU 살릴 때" 꺼내 쓰는 참고자료. 지금은 데스크탑 제작이 먼저.*
