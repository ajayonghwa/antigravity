# 워크스루: Solid Split CadQuery

SpaceClaim의 기하 분할 로직을 CadQuery를 사용하여 순수 파이썬 환경으로 성공적으로 마이그레이션하고 초기화를 완료했습니다.

## 🚀 주요 성과

1.  **프로젝트 기반 구축**: `core/`, `input/`, `output/`, `examples/`로 구성된 모듈형 구조를 생성했습니다.
2.  **핵심 로직 구현**:
    *   `geometry_utils.py`: 벡터 수학 및 바운딩 박스 연산 지원.
    *   `classifier.py`: 면 분류(Cylinder vs Plane) 및 내부/외부 감지 기초 로직 구현.
    *   `splitter.py`: CadQuery의 불리언 연산(`intersect`, `cut`)을 활용한 견고한 **O-Grid**, **평면 분할(Planar Split)**, **섹터 분할(Sector Split, 4분할)** 및 **H-Grid(병렬 슬라이싱)** 메서드 구현.
3.  **자동화 및 특징 감지**:
    *   `main.py`를 통해 `input/` 폴더 내의 STEP 파일을 자동으로 처리하는 엔트리 포인트를 제공합니다.
    *   `classifier.py`에 **주축(Main Axis) 감지** 로직을 추가하여 모델의 방향을 자동으로 파악합니다.
4.  **검증 완료**:
    *   `examples/demo_ogrid.py`: 실린더 생성 및 O-Grid 분할 검증.
    *   `examples/demo_advanced_splits.py`: 복합 형상에 대한 섹터 및 H-Grid 분할 연쇄 적용 검증.
    *   `examples/batch_process_and_report.py`: `validator/data` 내의 기존 예제들을 일괄 처리하고 시각화 보고서를 생성합니다.

## 🧪 검증 결과

### 1. O-Grid Split 데모
데모 스크립트 실행 시 두 개의 개별 STEP 파일이 생성됩니다.

### 2. 고급 분할(Sector & H-Grid) 데모
복합 형상을 4개의 쿼드런트로 나누고, 그 중 하나를 다시 여러 조각으로 슬라이싱하는 과정을 성공적으로 수행했습니다.

### 3. 시각화 분석 보고서 (HTML)
`validator/data`의 주요 예제들에 대해 분할 전/후의 모습을 **Top, Front, Isometric** 뷰로 렌더링한 HTML 보고서를 생성했습니다.
- **보고서 위치**: `solid_split_cadquery/examples/report/index.html`
- **주요 내용**: `auto_cylinder`, `auto_perforated`, `lv4_final_boss` 등 주요 모델의 분할 결과 시각화.

```bash
python3 examples/demo_ogrid.py
# 출력 결과:
# 🚀 Running O-Grid Split Demo...
#  - Applying O-Grid split (radius=30)...
# ✅ Demo finished. Check output/ for results:
```

## 📂 프로젝트 구조

```text
solid_split_cadquery/
├── core/
│   ├── classifier.py      # 특징 분석
│   ├── splitter.py        # O-Grid, 평면 분할 로직
│   └── geometry_utils.py  # 수학 유틸리티
├── examples/
│   └── demo_ogrid.py      # 검증 스크립트
├── input/                 # 분할할 .step 파일을 넣는 곳
├── output/                # 분할 결과 저장소
├── main.py                # 메인 실행 파일
└── README.md              # 프로젝트 문서
```

## 📝 향후 계획
- **Sector Split** 및 **H-Grid**와 같은 복잡한 전략 추가 구현.
- `Classifier` 기능을 강화하여 입력된 STEP 파일에서 O-Grid 대상을 자동으로 감지하는 기능 추가.
