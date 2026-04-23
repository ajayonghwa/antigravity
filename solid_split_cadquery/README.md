# 🧊 Antigravity: Autonomous Solid Decomposition Engine

본 프로젝트는 복잡한 3D 솔리드(STEP) 형상을 해석(FEA)용 육면체 격자(Hex-Mesh) 생성이 용이한 형태로 **자율 분할**하는 차세대 기하학적 엔진입니다.

## 🌟 핵심 컨셉: Adaptive Greedy Decomposition

단순히 미리 정해진 계획대로 자르는 것이 아니라, **"자르고 → 다시 분석하고 → 가장 높은 점수의 다음 후보 선택"** 의 반복 루프를 통해 매 이터레이션마다 최적 분할을 탐색합니다.  
엔진은 전체 형상을 사전에 파악(DNA 분석)한 뒤, 후보 절단 평면들을 생성하고, 각 분할의 Hex-Readiness 예상 점수를 비교하여 탐욕적으로 최선의 절단을 선택합니다.

---

## 📂 주요 디렉토리 및 파일 가이드

### 🧠 핵심 로직 (`core/`)
- **`classifier.py`**: 모델의 DNA 분석기. 구멍 위치·반지름·보스 여부·단차 등을 정밀 감지하여 글로벌 리포트를 생성합니다.
- **`strategy_planner.py`**: 프로젝트의 두뇌. 아래의 후보 전략들을 평가하고 최적 절단을 반복 실행합니다.
- **`splitter.py`**: 실제 절단 도구. CadQuery/OCCT 커널로 물리적 바디 분할을 수행합니다.

### 🧪 검증 및 예제 (`validator/`, `examples/`)
- **`engine.py`**: 분할 조각들의 Hex-Readiness 점수를 산출합니다.
- **`cad_generator.py`**: 테스트용 복합 형상(엘보우, 다공판, 단차 원판 등)을 자동 생성합니다.
- **`batch_process_and_report.py`**: 전체 입력 파일 배치 처리 및 결과 리포트 생성 스크립트입니다.

### 📁 데이터 관리
- **`input/`**: 분석할 `.step` 파일을 넣는 곳입니다.
- **`output/`**: 분할 완료된 개별 바디들이 저장됩니다.

---

## 📊 점수 체계 (Hex-Readiness Score)

각 분할 조각은 아래 4가지 지표의 가중 평균으로 평가됩니다:

| 지표 | 가중치 | 설명 |
|---|:---:|---|
| **Face Score** | 35% | 면 수가 6개(정육면체)에 가까울수록 높음 |
| **Orthogonality** | 35% | 면들이 서로 수직(직교)에 가까울수록 높음 |
| **Aspect Ratio** | 15% | 바운딩박스 비율이 정육면체에 가까울수록 높음 |
| **Skewness** | 15% | 면 법선이 X/Y/Z 주축에 정렬될수록 높음 |

**기준**: 80점 이상이면 Hex-Mesh 준비 완료로 판정

---

## 🛡️ 분할 후보 전략 및 우선순위

엔진은 분석된 바디마다 아래 후보들을 생성하고, 가중치(weight)가 높은 순서로 우선 평가합니다:

| 전략 | Weight | 설명 |
|---|:---:|---|
| **DISK_RADIUS** | **3.5** | OCP 기반 원통 반지름 추출 → ±R 위치에서 수직 절단, 동심원 영역 분리 |
| **DISK_SIDE** | **3.0** | 원통 면 2개 이상 바디의 중심 X/Y 수직 절단 |
| **HOLE_ISO** | **2.5** | 구멍 반지름 1.5배 거리에서 구멍 격리 |
| **SYMMETRY** | **2.0** | 전역 중심을 통과하는 X/Y/Z 대칭 절단 |
| **STEP** | **1.1** | 단차 면(Z평면) 절단 (최소 두께 10% 조건 충족 시) |

---

## 🔒 하드 제약 조건 (Hard Constraints)

분할은 아래 조건을 초과하면 해당 이터레이션을 중단합니다:

| 조건 | 기본값 | 설명 |
|---|:---:|---|
| **시간 제한** | 10초 | 케이스당 최대 실행 시간 |
| **바디 수 제한** | 30개 | 이 수 이상이 되면 분할 중단 |
| **최소 부피 비율** | 1/40 (0.025) | 이 비율 미만 조각 생성 시 패널티 |

---

## ⚠️ 페널티 시스템

최적 분할 선택 시 아래 조건을 위반하면 점수에 페널티를 부여합니다:

| 위반 조건 | 패널티 | 결과 |
|---|:---:|---|
| 조각 부피 < 최소 부피 비율 | 60% / 개 | 80점 → 1개 위반 시 32점 |
| 조각 Aspect Ratio > 8 (얇은 포) | 60% / 개 | 포 조각 방향 절단 자동 회피 |

---

## 🚀 사용법 (Quick Start)

1. **환경 설정**
   ```bash
   pip install -r requirements.txt
   ```

2. **입력 파일 준비**: `input/` 폴더에 STEP 파일을 넣습니다.

3. **단일 파일 분석**
   ```python
   import cadquery as cq
   from core.strategy_planner import StrategyPlanner
   from validator.engine import ValidationEngine

   model = cq.importers.importStep('input/your_model.step')
   planner = StrategyPlanner(model, max_bodies=30, max_time=10,
                             target_score=80, min_vol_ratio=0.025)
   results = planner.plan_and_execute()

   validator = ValidationEngine()
   report = validator.validate_split(model, results)
   print(f"평균 점수: {report['hex_readiness']['average_score']:.1f}")
   ```

4. **전체 배치 테스트**
   ```bash
   python examples/batch_process_and_report.py
   ```

5. **결과 확인**: `examples/report/index.html` 열기

---

## 📈 최근 개선 이력

| 버전 | 주요 변경 내용 |
|---|---|
| v1 | 기본 Greedy 분할 루프 + 스냅 어웨어 중복 제거 |
| v2 | Skewness 지표 추가 (가중치 15%), 점수 체계 4항목으로 재편 |
| v3 | 소체적 패널티 40%→60%, 얇은 조각(Aspect>8) 패널티 추가 |
| **v4** | **DISK_SIDE/DISK_RADIUS 후보 추가 + STEP 두께 필터 (10%)** |
|  | stepped disk 얇은 포 조각 6→1개, 평균 점수 85→91점 향상 |

---

**Note**: 본 엔진은 OpenCASCADE(OCP) 기술 기반이며, 사용자의 기하학적 통찰을 코드로 자동화하는 것을 목표로 합니다.
