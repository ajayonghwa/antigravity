# 📘 Solid Decomposer User Guide (v2.0)

본 가이드는 고도화된 규칙 기반 플래너와 AI 지능형 플래너를 활용하여 복잡한 3D 형상을 분할하는 방법을 설명합니다.

## 1. 개요 (Dual-Engine Strategy)
본 시스템은 두 가지 엔진을 제공합니다.
- **Rule-based Engine (Default)**: 초고속 기하학 수식을 이용한 분할. (대부분의 표준 형상에 권장)
- **AI-driven Engine (Advanced)**: Gemma 모델을 이용한 추론 기반 분할. (매우 복잡한 비정형 형상에 권장)

---

## 2. 사용 방법

### A. 일반 모드 (빠른 실행)
표준적인 다공판, 파이프, 샤프트 형상에 사용합니다.
```bash
python main_run.py [파일이름]
```
- **특징**: 1초 내외로 완료. 0.01mm 오프셋 로직으로 위상 에러가 방지됨.

### B. AI 지능형 모드 (선택 사항)
기울어진 접합부나 복합적인 보스급 형상에서 규칙 기반 플래너가 만족스럽지 않을 때 사용합니다.
```bash
python main_run.py [파일이름] --ai
```
- **사전 요구사항**: 로컬에 `ollama` 및 `gemma4:e4b` 모델이 설치되어 있어야 함.
- **특징**: AI가 형상을 분석하여 최적의 분할 계획을 JSON으로 제안함 (약 1~2분 소요).

---

## 3. 주요 개선 사항 (v2.0)
- **Topological Safety**: 십자 분할 시 0.01mm 미세 이동을 통해 SpaceClaim 커널 에러를 원천 봉쇄함.
- **Feature-Aware Axial Splits**: 단차뿐만 아니라 테이퍼 구간 등 모든 주요 기하학적 변화 지점을 자동으로 포착하여 격리함.
- **Angled Junction Support**: 기울어진 파이프(Y-Junction)에 대해 로컬 축 기반의 수직 분할(Transverse Split)을 자동 적용함.

---

## 4. 문제 해결 (Troubleshooting)
- **Unable to split body 에러**: 
    - 형상이 너무 미세하게 겹쳐있을 때 발생합니다. 
    - `strategy_planner.py`에서 `threshold_radius` 수치를 조절하여 작은 구멍을 필터링하세요.
- **Gemma 응답 지연**: 
    - 보스 레벨 형상은 데이터량이 많아 시간이 걸릴 수 있습니다. 터미널의 "Thinking..." 메시지를 기다려 주세요.

---
*Created by Antigravity AI Agent*
