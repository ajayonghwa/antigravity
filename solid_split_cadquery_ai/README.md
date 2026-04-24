# Solid Split AI - autonomous Geometric Decomposition

이 프로젝트는 AI 기반의 기하학적 특징 분석을 통해 유한요소해석(FEA)용 헥사메쉬(Hex-mesh) 생성을 위한 솔리드 분할을 자동화하는 엔진입니다.

## 🚀 주요 기능
- **기능 기반 형상 인식**: 구멍(Hole), 단차(Step), 튜브(Tube), 접합부(Junction) 자동 추출.
- **AI 전략 수립**: 추출된 피처를 바탕으로 AI가 최적의 절단면(Cut Plane) 결정.
- **자동 분할 실행**: CadQuery를 이용한 고정밀 솔리드 절단.
- **다중 뷰 시각화 리포트**: 분할 전후의 정면/측면/등각뷰를 비교하는 HTML/MD 리포트 자동 생성.

## 🛠 설치 방법
```bash
pip install -r requirements.txt
```

## 💻 사용 방법
### 단일 파일 처리 (추천)
외부 STEP 파일을 입력받아 분석 및 분할을 수행하고 리포트와 조각 파일들을 생성합니다.
```bash
# 기본 실행
python3 main.py [input_file.step] --output [report_folder]

# 안전 제약 조건 적용 실행 (조각 수 제한 및 최소 부피 설정)
python3 main.py [input_file.step] --max-parts 15 --min-volume 0.05
```

## 🛡️ 안전 제약 조건 (Safety Constraints)
AI의 과도한 분할을 방지하기 위한 기능입니다:
- `--max-parts`: 한 바디가 분할될 수 있는 최대 조각 수를 제한합니다.
- `--min-volume`: 원본 부피 대비 특정 비율(예: 0.05 = 5%) 미만의 너무 작은 조각이 생기면 경고를 발생시킵니다.

## 📊 결과 확인
- **분할된 STEP 파일**: `[output_folder]/parts/` 폴더 내에 각 조각이 저장됩니다.
- **HTML 리포트**: `[output_folder]/index.html`을 브라우저로 열면 3D 뷰 및 다중 뷰 비교를 확인할 수 있습니다.
- **문서 리포트**: `[output_folder]/decomposition_report.md`에서 AI의 판단 근거를 확인할 수 있습니다.

---
*Developed by Gemini Solid-Split Engine*
