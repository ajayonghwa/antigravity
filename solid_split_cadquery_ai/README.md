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
외부 STEP 파일을 입력받아 분석 및 분할을 수행하고 리포트를 생성합니다.
```bash
python3 main.py [input_file.step] --output [report_folder]
```

### 데모 및 배치 테스트
```bash
# 단일 복합 형상 데모 실행
python3 demo_full_pipeline.py

# 3종 복합 형상 배치 처리
python3 batch_ai_pipeline.py
```

## 🧠 로컬 AI (Ollama) 연동 가이드
프로젝트를 실제 로컬 LLM과 연동하려면 다음 단계를 따르세요:

1. **Ollama 실행**: `ollama run llama3` (또는 mistral 등)
2. **src/planner.py 수정**: 
   - `requests` 모듈을 사용하여 `http://localhost:11434/api/generate`로 JSON 요약을 전달합니다.
   - 프롬프트에 "결과를 반드시 JSON 형식의 `splits` 배열로 응답하라"는 지시를 포함하세요.
3. **main.py 수정**:
   - `ai_plan` 하드코딩 부분을 `planner.plan_strategy(summary)` 호출로 교체합니다.

## 📊 결과 확인
- **HTML 리포트**: `[output_folder]/index.html`을 브라우저로 열면 3D 뷰 및 다중 뷰 비교를 확인할 수 있습니다.
- **문서 리포트**: `[output_folder]/decomposition_report.md`에서 AI의 판단 근거를 확인할 수 있습니다.

---
*Developed by Gemini Solid-Split Engine*
