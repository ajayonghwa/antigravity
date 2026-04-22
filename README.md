# 📘 Solid Decomposer: Automated CAD Partitioning Pipeline (v2.2)

본 프로젝트는 복잡한 3D 형상을 해석 및 메쉬 최적화를 위해 자동으로 분할하는 통합 자동화 시스템입니다. 

## 🚀 핵심 기능 (Key Features)

### 1. Dual-Engine Strategy
- **Rule-based Engine (Default)**: 기하학적 수식을 이용한 초고속 분할. 표준 형상(Cylinder, Stepped, Perforated)에 최적화.
- **AI-driven Engine (Advanced)**: Gemma 모델을 이용한 지능형 추론 분할. 복잡한 비정형 형상 및 접합부(Junction)에 권장.

### 2. 🛡️ Robust Partitioning Logic (v2.2 New!)
- **Sequential Splitting & Name Matching**: 이름 뒤에 숫자가 붙는(Solid11 등) 모든 파생 조각을 추적하여 누락 없는 순차 분할을 보장합니다.
- **Sliver Prevention (Z-Merge)**: 0.5mm 이하의 미세한 단차는 지능적으로 하나로 병합하여, 해석 시 에러를 유발하는 얇은 조각(Sliver body) 생성을 방지합니다.
- **Tapered Shape Support**: 원기둥뿐만 아니라 테이퍼진 원뿔(Conical) 구간을 자동으로 포착하여 단차 구역을 격리합니다.

### 3. 🕸️ High-Quality Mesh Foundation
- **Multi-Coaxial O-grid**: 이중 관이나 다중 동축 구멍이 있는 경우, 모든 층에 대해 겹겹이 O-grid를 생성하여 최상의 Hexa 메쉬 기반을 마련합니다.
- **Symmetry Intelligence**: 모델의 원점 대칭 여부를 자동 감지하여 1/4, 1/8 모델 활용을 통한 해석 시간 단축 가이드를 제공합니다.

### 4. 📖 Automated Human Guide
- 스페이스클레임 스크립트 생성 시, 동일한 위치에 **`Decomposition_Guide.md`**가 자동으로 생성됩니다. 
- 자동화가 어려운 특수한 상황에서 엔지니어가 직접 보고 따라 할 수 있는 Step-by-Step 지침을 제공합니다.

---

## 📂 폴더 구조

- **`01_extractor/`**: SpaceClaim 기하 정보 추출 엔진. (Conical 및 is_internal 판별 지원)
- **`02_planner/`**: 분할 전략 수립. (Z-Merge 및 다중 O-grid 지능 탑재)
- **`03_generator/`**: 순차 분할 및 자식 바디 추적 로직이 적용된 스크립트 생성기.
- **`validator/`**: CadQuery 기반의 형상/위상 자동 검증 도구.

---

## 🛠️ 사용 방법

```bash
# 기본 실행 (규칙 기반)
python main_run.py [파일이름]

# AI 모드 실행
python main_run.py [파일이름] --ai
```

---
*Created by Antigravity AI Coding Assistant*
