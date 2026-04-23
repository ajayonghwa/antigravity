# 🧊 Antigravity: Autonomous Solid Decomposition Engine

본 프로젝트는 복잡한 3D 솔리드(STEP) 형상을 해석(FEA)용 육면체 격자(Hex-Mesh) 생성이 용이한 형태로 **자율 분할**하는 차세대 기하학적 엔진입니다.

## 🌟 핵심 컨셉: Adaptive Recursive Strategy
단순히 미리 정해진 계획대로 자르는 것이 아니라, **"자르고 -> 다시 분석하고 -> 다시 계획 세우기"**의 재귀적 루프를 통해 기하학적 꼬임과 뾰족한 형상(Sliver) 발생을 원천 차단합니다.

## 📂 주요 디렉토리 및 파일 가이드

### 🧠 핵심 로직 (`core/`)
- **`classifier.py`**: 모델의 유전자(DNA) 분석기. 구멍의 위치, 반지름, 보스(Boss) 여부, 단차 등을 정밀하게 감지하여 리포트를 생성합니다.
- **`strategy_planner.py`**: 이 프로젝트의 '두뇌'. 재귀적 루프를 돌며 각 조각에 최적인 분할 전략(사각 격리, O-Grid, 섹터 분할 등)을 결정합니다.
- **`splitter.py`**: 실제 절단 도구. CadQuery/OCCT 커널을 사용하여 물리적으로 바디를 분할합니다.

### 🧪 검증 및 예제 (`validator/`, `examples/`)
- **`engine.py`**: 분할된 조각들의 Hex-Readiness(격자 생성 준비도) 점수를 산출합니다. (곡면 허용 스코어링 적용)
- **`cad_generator.py`**: 테스트를 위한 복합 형상(엘보우, 다공판, 단차 원판 등)을 자동으로 생성합니다.
- **`batch_process_and_report.py`**: 모든 입력 파일을 분석하고 HTML 리포트를 생성하는 통합 스크립트입니다.

### 📁 데이터 관리
- **`input/`**: 분석하려는 `.step` 파일을 넣는 곳입니다.
- **`output/`**: 분할이 완료된 개별 바디들이 저장됩니다.
- **`data/test_reference/`**: 테스트 및 검증을 위한 참조 데이터가 보관됩니다.

## 🚀 사용법 (Quick Start)

1. **환경 설정**: `requirements.txt`를 통해 필요한 라이브러리(CadQuery 등)를 설치합니다.
2. **입력 파일 준비**: `input/` 폴더에 원하는 STEP 파일을 넣습니다.
3. **분석 및 리포트 생성**:
   ```bash
   python examples/batch_process_and_report.py
   ```
4. **결과 확인**: `examples/report/index.html`을 열어 점수와 분할 형상을 확인합니다.

## 🛡️ 주요 분할 전략
- **Square Isolation**: 구멍 주변을 정사각형으로 먼저 격리하여 Sliver 발생 방지.
- **Elbow Path Split**: 곡면 파이프의 경로를 분석하여 곡률 중심 기준 분할.
- **Sector Split**: 원통형 바디를 90도 quadrants로 나누어 격자 품질 최적화.
- **Z-Partitioning**: 내부 단차 및 격벽을 탐지하여 층별로 분리.

---
**Note**: 본 엔진은 OpenCASCADE 기술을 기반으로 하며, 사용자의 기하학적 통찰을 코드로 자동화하는 것을 목표로 합니다.
