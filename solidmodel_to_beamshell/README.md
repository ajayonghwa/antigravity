# SolidModel to BeamShell Automation Pipeline

본 프로젝트는 3D 솔리드 형상을 분석하여 빔/쉘 기반의 축약 모델(ROM)을 생성하고, 해석 결과와 일치하도록 자동 최적화하는 통합 시스템입니다.

## 📁 폴더 구조 및 작업 순서

모든 작업은 순차적으로 진행되며, 각 폴더의 번호가 실행 순서를 나타냅니다.

### 01_apdl_checker
- **목표:** LLM이 작성한 APDL 코드의 문법 및 논리 오류 검증.
- **주요 파일:** `apdl_checker.py`, `rules.json`

### 02_geometry_extractor
- **목표:** SpaceClaim에서 각 구역별 질량, 단면 치수, 물성치 추출.
- **주요 파일:** `extract_manager.py`, `scdm_script_template.py`

### 03_model_generator
- **목표:** 추출된 데이터를 기반으로 변수화된 APDL 모델 생성.
- **주요 파일:** `model_builder.py` (우산형 원판 모델링 지원)

### 04_optimization_tuning
- **목표:** 3D 해석 결과(RST)와 비교하여 파라미터 최적화.
- **주요 파일:** `tuning_engine.py`, `mode_mapper.py`

---

## 🐍 가상환경 설정 (Windows / Mac)

본 프로젝트는 독립된 가상환경을 사용합니다.

1. **가상환경 활성화:**
   - Windows: `.\.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

2. **라이브러리 확인:** `pandas`, `scipy`, `numpy`, `ansys-dpf-core` 등이 설치되어 있습니다.

---

## 🚀 실행 가이드

1. **Step 1:** `02_geometry_extractor`를 통해 3D 모델 정보를 `final_parameters.csv`로 추출합니다.
2. **Step 2:** `03_model_generator`를 실행하여 `base_model.dat`을 생성합니다.
3. **Step 3:** `04_optimization_tuning`에서 3D 해석 결과(`.rst`)의 **절대 경로**를 지정하여 매퍼를 실행하고 정답 데이터를 생성합니다.
4. **Step 4:** `opt_config.json`에서 가중치, RST 경로, 그리고 **튜닝 모드**를 설정한 후 `tuning_engine.py`를 실행합니다.

### ⚙️ 튜닝 모드 설정 (`opt_config.json`)

- **`"tuning_mode": "light"`**: 주파수와 유효질량 위주로 빠르게 튜닝합니다. (초기 모델 정합성 확인용)
- **`"tuning_mode": "full"`**: 주파수, 유효질량에 더해 **MAC(모드 형상)**까지 정밀하게 맞춥니다. (최종 검증용)
