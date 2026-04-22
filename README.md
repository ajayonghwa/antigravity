# 📘 Solid Decomposer: Automated CAD Partitioning Pipeline (v2.1)

본 프로젝트는 복잡한 3D 형상을 해석 및 메쉬 최적화를 위해 자동으로 분할하는 통합 자동화 시스템입니다. 

## 🚀 핵심 기능 (Key Features)

### 1. Dual-Engine Strategy
- **Rule-based Engine (Default)**: 기하학적 수식을 이용한 초고속 분할. 표준 형상(Cylinder, Stepped, Perforated)에 최적화.
- **AI-driven Engine (Advanced)**: Gemma 모델을 이용한 지능형 추론 분할. 복잡한 비정형 형상 및 접합부(Junction)에 권장.

### 2. 🛡️ Topological Reliability (Bug Fix)
- **Sequential Splitting**: 일괄 분할 시 일부 조각이 누락되는 현상(3조각 버그)을 해결하기 위해 **순차적 분할 및 계보 추적(Ancestry Tracking)** 로직을 도입하여 100% 분할 성공률을 보장합니다.
- **0.01mm Offset Safety**: 수치적 불안정성으로 인한 커널 에러를 방지하기 위해 미세 오프셋 로직이 적용되어 있습니다.

### 3. 📖 Automated Human Guide
- 스페이스클레임 스크립트 생성 시, 동일한 위치에 **`Decomposition_Guide.md`**가 자동으로 생성됩니다. 
- 자동화가 어려운 특수한 상황에서 엔지니어가 직접 보고 따라 할 수 있는 Step-by-Step 지침을 제공합니다.

---

## 📂 폴더 구조

- **`01_extractor/`**: SpaceClaim 기하 정보 추출 엔진.
- **`02_planner/`**: 분할 전략 수립 (Rule-based / AI).
- **`03_generator/`**: **(핵심)** 순차 분할 로직이 적용된 IronPython 스크립트 생성기.
- **`scdm_bridge/`**: 맥북 환경에서의 시뮬레이션 및 안전 API 래퍼.
- **`validator/`**: CadQuery 기반의 형상/위상 자동 검증 도구.

---

## 🛠️ 사용 방법

```bash
# 기본 실행 (규칙 기반)
python main_run.py [파일이름]

# AI 모드 실행
python main_run.py [파일이름] --ai
```

결과물은 `04_scripts/` 폴더 내에 `final_scdm_script.py`와 `Decomposition_Guide.md`로 저장됩니다.

---
*Created by Antigravity AI Coding Assistant*
