# AntiGravity: SCDM Solid Decomposer 🚀

SpaceClaim(SCDM) 기하 형상을 분석하고 구조/유동 해석을 위한 육면체 격자(Hexahedral Mesh) 생성을 돕도록, 복잡한 솔리드 바디를 자동으로 분할(Decomposition)해주는 파이프라인 툴킷입니다. 현재 버전 **v3.1**로 업그레이드되어 복잡한 7대 실무 형상까지 완벽히 대응합니다.

---

## 🎯 핵심 목표 (Core Objectives)
- 수작업에 의존하던 지루하고 반복적인 SpaceClaim 기하 분할 작업 자동화
- Sweep 및 MultiZone Method에 완벽하게 대응되는 고품질 육면체(Hexa-core) 서브 바디 생성
- 이름 충돌, 패턴 바디 연쇄 변형 등 SCDM API 고질적 문제 해결

## 🌟 주요 기능 (v3.1)

### 1. 7대 실무 형상 맞춤형 전략 (Classifier & Strategy)
단순한 O-Grid 생성을 넘어, 바디의 기하학적 특성을 7가지로 분류하여 맞춤형 분할 전략을 실행합니다.
1. **다공판 (Perforated Plate)**: H-Grid 매트릭스로 구멍 사전 격리 후 O-Grid 적용
2. **단차 원판 (Stepped Disk)**: 직경 변화점에 횡단면 분할 후 90도 Sector 분할
3. **엘보우 (Elbow)**: 곡면 시작/끝점 감지 및 횡단면(Sweep Path) 분할
4. **크로스 홀 (Cross Hole)**: Sector 각도를 45도 틀어 측면 구멍 파괴 회피
5. **얇은 원통 (Thin-walled)**: O-Grid 생략 및 Sector를 통한 Sweep 유도
6. **볼트/와셔 (Fastener)**: Bounding Box 기준 극소형 부품 복잡 분할 생략
7. **돌출 블록 (Boss)**: 밑면을 연장해 실린더 외벽에서 사전 분리 (Boss Separation)

### 2. 지능형 메쉬 품질 제어 (WHR)
*   **Wall-to-Hole Ratio (WHR)**: 구멍과 외벽 사이의 거리를 측정하여 메쉬 찌그러짐을 방지합니다.
    *   WHR < 1.0 (벽에 너무 가까움): 반원형 C-Grid 혹은 O-Grid 생략
    *   1.0 ~ 6.0 (적정 거리): O-Grid 적용
    *   WHR > 6.0 (너무 멀음): 자유 메쉬에 맡기기 위해 O-Grid 생략
*   *예외 사항*: 직경 50mm 이상의 대형 홀은 WHR 무관하게 무조건 강제 O-Grid 코어 생성.

### 3. 무결성 방어 체계 (Bulletproof Integrity)
*   **이름 충돌 3단계 방어**: 여러 부품이 섞여 있을 때 `Rename -> Attribute -> Fingerprint(Volume+BBox 해시)` 3단계 폴백(Fallback) 추적 기법을 사용해 정확한 타겟 바디만 잘라냅니다.
*   **동적 커터 스케일링**: 모델 전체의 Bounding Box 대각선 길이를 계산해, 커터가 어떤 크기의 모델이든 완벽하게 두 동강 낼 수 있도록 동적으로 크기를 늘립니다.
*   **패턴 바디 안전화**: SCDM의 인스턴스(Pattern) 공유 특성으로 인해 한 바디를 자를 때 다른 바디가 파괴되는 문제를 막고자, 스크립트 실행 전 모든 바디를 복사 후 원본 삭제 방식으로 독립(Independent) 바디로 만듭니다.

---

## 📂 디렉토리 구조 (Architecture)

파이프라인은 3단계 독립 모듈 구조로 되어 있습니다.

```text
solid_decomposer/
├── 01_extractor/               # (1) SCDM 스크립트로 기하 정보(Face, Box) 추출
│   └── scdm_extractor.py       # (JSON 직렬화 및 이름 3단계 방어 체계 포함)
├── 02_planner/                 # (2) 파이썬 코어 로직. 기하 분석 및 분할 전략 수립
│   └── strategy_planner.py     # (7대 형상 분류기 및 WHR 기반 분할 계획 생성)
├── 03_generator/               # (3) 수립된 계획을 다시 SCDM 파이썬 스크립트로 변환
│   └── scdm_generator.py       # (패턴 독립화, 동적 커터 생성, SplitBody API 호출)
├── scdm_bridge/                # 브릿지 도구 및 가이드 자동 생성기
│   └── guide_generator.py      # 사람이 읽기 쉬운 Markdown 가이드 생성
├── 04_scripts/                 # (결과물) 최종 생성된 SCDM 실행 스크립트가 저장되는 곳
└── SCDM_Automation_Troubleshooting_Guide.md # 필수 트러블슈팅 및 엔진 지침서
```

## 🛠️ 실행 방법 (Workflow)

1. **SpaceClaim에서 기하 추출:**
   - SpaceClaim 스크립트 창에서 `01_extractor/scdm_extractor.py`의 코드를 복사해서 실행합니다.
   - `geometry_data_block.json` 파일이 생성됩니다.
2. **전략 수립 및 스크립트 생성:**
   - 터미널(가상환경 활성화)에서 `python main_run.py` (또는 통합 실행 스크립트)를 실행합니다.
   - 플래너가 기하학적 특성을 분석하고 `04_scripts/scdm_decomposition_script.py` 파일을 생성합니다.
3. **SpaceClaim에서 분할 실행:**
   - 다시 SpaceClaim 스크립트 창으로 돌아와 `04_scripts/scdm_decomposition_script.py`의 코드를 복사해서 실행합니다.
   - 기하가 기가 막히게 분할되는 모습을 감상합니다.

## 📖 트러블슈팅
API 참조 오류, SplitBody 4인자 에러 등 SpaceClaim 파이프라인 개발 중 겪을 수 있는 모든 이슈와 원인, 극복 방법은 `SCDM_Automation_Troubleshooting_Guide.md`에 아주 상세히 기록되어 있습니다. 코드를 수정하기 전 반드시 읽어보세요.

---
*Powered by AntiGravity Project Team*
