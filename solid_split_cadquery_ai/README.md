# 🧊 Solid Split CadQuery AI

AI 기반의 유한요소해석(FEA) 전처리용 솔리드 분할 엔진입니다.

## 🚀 프로젝트 개요
이 프로젝트는 복잡한 3D 솔리드를 육면체 격자(Hex-Mesh) 생성이 용이한 형태로 자동 분할합니다. 사용자님의 지적처럼 아래 3가지 핵심 관점에 집중하여 설계되었습니다:

1.  **정밀한 형상 인식 (Feature Extraction)**: CadQuery를 통해 모델의 DNA(구멍, 단차, 크기)를 추출하여 AI에게 전달합니다.
2.  **구조화된 AI 계획 (AI Planning)**: 로컬 LLM이 JSON 형식으로 실행 가능한 분할 명령을 생성합니다.
3.  **정확한 기하 연산 (Geometric Execution)**: 생성된 계획에 따라 CadQuery가 물리적 분할을 수행합니다.

## 🛠️ 핵심 모듈 설명

### 1. 형상 추출기 (`src/extractor.py`)
*   **역할**: 솔리드 모델을 분석하여 AI가 이해할 수 있는 JSON 요약본을 만듭니다.
*   **주요 기능**: 전체 크기 측정, 구멍 패턴(반지름, 위치, 개수) 감지, 단차(Step) 레벨 분석.

### 2. AI 플래너 (`src/planner.py`)
*   **역할**: 요약된 정보를 바탕으로 최적의 분할 전략을 수립합니다.
*   **주요 기능**: 로컬 AI(Ollama 등)와 통신, 실행 가능한 JSON 명령 세트(`splits`) 생성.

### 3. 분할 실행기 (`src/executor.py`)
*   **역할**: AI의 명령을 받아 실제 CadQuery 코드로 변환하여 실행합니다.
*   **주요 기능**: 평면 절단(`plane_cut`), 구멍 격리(`hole_isolation`), 결과물 저장.

## 📦 설치 방법
```bash
pip install -r requirements.txt
```

## 📖 사용법
1.  분석할 `.step` 파일을 `data/input/` 폴더에 넣습니다.
2.  메인 파이프라인을 실행합니다:
    ```bash
    python main.py
    ```
3.  `data/output/` 폴더에서 분할된 결과물을 확인합니다.

## 🤖 AI 설정
본 엔진은 `http://localhost:11434`에서 실행 중인 로컬 AI 서버(예: Ollama)를 기본으로 사용합니다.
기본 모델: `llama3` (변경 가능: `src/planner.py`)
