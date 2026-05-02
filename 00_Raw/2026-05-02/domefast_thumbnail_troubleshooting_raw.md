# 2026-05-02 Domefast Thumbnail Troubleshooting Raw

도매매나 도매꾹의 상품 이미지들은 배경에 화려한 홍보 텍스트, 그림자, 복잡한 소품들이 섞여 있는 경우가 많습니다. 현재 사용 중이신 **`rembg`의 기본 모델(`u2net`)은 이러한 이커머스 이미지에 취약**하여, 말씀하신 대로 제품이 파먹히거나 쓸데없는 배경 찌꺼기가 남는 현상이 흔하게 발생합니다.

쿠팡이나 스마트스토어에 바로 등록할 수 있는 **'최상의 썸네일'을 자동으로 만들어내기 위해, 현재 파이썬 프로그램(`worker.py` 등)에 즉시 적용할 수 있는 4단계 해결책**을 제안해 드립니다.

---

### 💡 1단계: 가장 빠르고 쉬운 조치 (`rembg` 모델 & 옵션 튜닝)
가장 먼저 `rembg`의 기본 모델을 범용 사물이 아닌 **고해상도 객체 분리에 특화된 모델**로 변경하고, 경계선을 다듬는 옵션을 추가해야 합니다.

*   **모델 변경:** `isnet-general-use` 모델을 사용하면 테두리를 훨씬 정교하게 따냅니다.
*   **Alpha Matting 활성화:** 테두리의 계단 현상을 줄이고 파먹힘 현상을 방지합니다.

**💻 파이썬 코드 적용 예시:**
```python
from rembg import remove, new_session
from PIL import Image

# 1. 이커머스 객체 추출에 강한 'isnet-general-use' 세션 생성
# (최초 실행 시 가중치 파일을 자동 다운로드합니다. Batch 처리 시 세션은 한 번만 생성하여 재사용하세요!)
session = new_session("isnet-general-use") 

input_image = Image.open('input.jpg')

# 2. 알파 매팅을 적용하여 찌꺼기 제거 및 파먹힘 방지
output_image = remove(
    input_image, 
    session=session,
    alpha_matting=True, 
    alpha_matting_foreground_threshold=240, # 이 값을 조절하여 파먹힘 방지
    alpha_matting_background_threshold=10,  # 배경 찌꺼기 제거
    alpha_matting_erode_size=10             # 경계선 다듬기 두께
)
```

### 💡 2단계: 최상의 오픈소스 AI로 엔진 교체 (BRIA RMBG-1.4)
만약 `rembg`를 튜닝해도 만족스럽지 않다면, 현재 이커머스 누끼 영역에서 **압도적인 1위인 BRIA AI의 `RMBG-1.4` 모델**로 엔진 자체를 교체하는 것을 강력히 추천합니다.
* 수백만 장의 '상업용 상품 이미지'로만 학습되어 있어, 도매매의 악조건 속에서도 상품만 기가 막히게 분리해 냅니다. 투명한 유리병이나 복잡한 자전거 스포크 등도 잘 분리합니다.
* 파이썬 `transformers` 라이브러리를 통해 로컬 데스크톱 앱 내부에 통합이 가능합니다.

### 💡 3단계: [⭐핵심] 필수 썸네일 후처리 파이프라인 추가
배경을 투명하게 잘 지웠다고 해도, 한쪽으로 치우쳐 있거나 투명한 여백이 많으면 상품이 볼품없어 보입니다. 쿠팡/스마트스토어 가이드라인에 맞춘 **스마트 패딩(Smart Padding) 후처리 로직**이 반드시 추가되어야 합니다.

1. **Auto Crop:** 누끼가 따진 이미지에서 의미 없는 투명 여백을 바짝 잘라냅니다.
2. **화이트 캔버스 & 정중앙 배치:** `1000 x 1000` 해상도의 순백색(`#FFFFFF`) 캔버스를 만들고, 상품을 약 85% 크기로 줄여 **정중앙에 배치**합니다.

**💻 Pillow(PIL) 적용 코드 예시:**
```python
from PIL import Image

def create_market_thumbnail(transparent_img, output_path, canvas_size=1000, margin_ratio=0.85):
    # 1. 투명 배경 이미지에서 실제 상품(픽셀이 있는 곳)만 타이트하게 자르기 (Auto-Crop)
    bbox = transparent_img.getbbox()
    if bbox:
        transparent_img = transparent_img.crop(bbox)
        
    # 2. 1000x1000 순백색 캔버스 생성
    canvas = Image.new('RGB', (canvas_size, canvas_size), (255, 255, 255))
    
    # 3. 마진(여백)을 고려하여 상품 리사이징 (예: 1000px의 85%인 850px에 맞춤)
    target_size = int(canvas_size * margin_ratio)
    transparent_img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
    
    # 4. 정중앙 좌표 계산 및 합성 (투명 알파 채널을 마스크로 사용)
    offset_x = (canvas_size - transparent_img.width) // 2
    offset_y = (canvas_size - transparent_img.height) // 2
    canvas.paste(transparent_img, (offset_x, offset_y), transparent_img)
    
    # 5. 최종 썸네일 저장 (JPEG로 저장하여 용량 최적화)
    canvas.save(output_path, 'JPEG', quality=95)
```

### 💡 4단계: UI 상에 "우회(Bypass) 옵션" 추가 (안전장치)
아무리 AI가 뛰어나도 100% 완벽할 수는 없습니다. 너무 난해한 도매매 이미지는 억지로 누끼를 따면 기괴해집니다.
* **해결책:** `main_desktop.py` UI에 **[라디오 버튼: 1. AI 배경 제거 및 썸네일 최적화 / 2. 원본 이미지 그대로 사용]** 옵션을 만들어 두세요. 유저가 엑셀 데이터의 상태에 따라 선택할 수 있게 우회로를 열어두면 클레임이 확 줄어듭니다.

---

### 📝 현재 마크다운 문서(작업 히스토리) 업데이트 제안

현재 작성 중이신 마크다운의 **`## 🚀 향후 과제 (To-Do)`** 섹션에 아래 내용을 추가하여 유부장님(또는 팀원)과 다음 스텝을 진행해 보세요!

```markdown
## 🚀 향후 과제 (To-Do)

### 5. 상품 썸네일 고도화 및 후처리 파이프라인 구축 (최우선 과제)
- **배경 제거(Rembg) 엔진 튜닝:** 기존 `u2net` 모델에서 이커머스 객체 분리에 특화된 `isnet-general-use` 모델로 변경 및 `Alpha Matting` 활성화를 통해 제품 테두리 파먹힘 현상 최소화.
- **오토 패딩(Smart Padding) 로직 추가:** 누끼 추출 후 투명 이미지를 그대로 쓰지 않고, Bounding Box 크롭 후 쿠팡/스마트스토어 규격인 `1000x1000` 순백색 캔버스 정중앙에 85% 비율로 자동 배치하는 Pillow(PIL) 후처리 스크립트 작성.
- **안전장치 UI 추가:** 누끼 제거가 불가능한 복잡한 연출 컷을 위해 엑셀 배치 시작 전, 'AI 배경 제거'와 '원본 이미지 유지'를 선택할 수 있는 라디오 버튼 추가.

### 6. 시스템 안정화 및 배포
- 수정된 `main_desktop.py`, `worker.py` 및 신규 아이콘이 반영된 최종 버전의 `domeggook_tool.exe` PyInstaller 재빌드 및 GitHub Release 덮어쓰기.
- 실제 도매매 대량 엑셀 데이터를 바탕으로 장시간 동작 시 메모리 누수 여부 모니터링 (특히 `rembg` session 객체의 싱글톤(Singleton) 재사용 여부 점검).
```

당장 **1단계(isnet 모델 변경)**와 **3단계(후처리 코드)**만 파이썬 코드에 적용하셔도 현재 느끼시는 썸네일 품질 불만의 80% 이상은 즉각적으로 해결되실 겁니다!
