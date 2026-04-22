# 🚀 Antigravity: Solid Decomposition & Optimization Pipeline

**Antigravity**는 복잡한 3D Solid 기하 모델을 해석 효율이 극대화된 형태로 자동 분할하고 최적화하는 통합 엔지니어링 솔루션입니다. 특히 SpaceClaim(SCDM) 환경에서의 Hexa-Mesh 기반을 마련하기 위한 지능형 분할 전략을 제공합니다.

---

## 🛠️ Core Components

본 프로젝트는 다음과 같은 유기적인 컴포넌트들로 구성되어 있습니다.

### 1. 🔍 Geometry Engine (`01_extractor` & `scdm_bridge`)
- **Smart Extraction**: SpaceClaim 내부 기하 정보를 JSON 형태로 정밀 추출합니다.
- **Conical & internal Detection**: 단순 원통을 넘어 테이퍼진 형상과 내부 유로(Internal flow)를 자동으로 판별합니다.
- **Bridge**: 외부 환경과 SCDM 간의 원활한 데이터 교환을 지원합니다.

### 2. 🧠 Strategy Planner (`02_planner` & `optimizer`)
- **O-Grid Intelligence**: 구멍 주변의 메쉬 품질을 높이기 위한 O-Grid 분할 전략을 수립합니다.
- **Partitioning Logic**: 90도 섹터 분할, 축 방향 단차 분할 등 최적의 Partition 순서를 결정합니다.
- **Strategy Optimization**: 여러 분할 시나리오 중 해석 리소스를 최소화할 수 있는 최적의 안을 선정합니다.

### 3. 🏗️ Script Generator (`03_generator`)
- **Robust Execution**: 사용자 환경의 API 버전(V17~V22)을 자동 감지하고 최적화된 시그니처로 스크립트를 생성합니다.
- **Surface Cutter Strategy**: `Fill` 및 `Extrude`를 활용한 서피스 기반 커팅으로 기하학적 연산 성공률을 극대화합니다.
- **Body Tracking**: 분할 후 이름이 바뀌는 모든 조각을 끝까지 추적하여 연속적인 분할을 수행합니다.

### 4. 🛡️ Validator & Executor (`validator` & `executor`)
- **Geometric Validation**: 분할된 결과물이 해석에 적합한지, 간섭이나 유실은 없는지 기하학적으로 검증합니다.
- **Auto-Run**: 생성된 스크립트를 SCDM에서 자동으로 실행하고 결과를 취합합니다.

---

## 📂 폴더 구조

```text
/antigravity
├── solid_decomposer
│   ├── 01_extractor     # SCDM 기하 정보 추출 엔진
│   ├── 02_planner       # 분할 전략 수립 엔진
│   ├── 03_generator     # SCDM 실행 스크립트 생성기
│   ├── validator        # 분할 결과 기하 검증 모듈
│   ├── optimizer        # 분할 시나리오 최적화 엔진
│   ├── scdm_bridge      # 외부-SCDM 통신 레이어
│   ├── main_run.py      # 파이프라인 통합 실행 엔트리
│   └── stable_v1_backup # [중요] 검증된 안정 버전 백업 (참고용)
└── doc_assistant        # 엔지니어링 문서화 지원 도구
```

---

## 💡 개발 및 트러블슈팅 가이드
SCDM API의 특이사항이나 빈번하게 발생하는 에러 해결 방법은 다음 문서를 참고하세요.
- **[Troubleshooting Guide](solid_decomposer/SCDM_Automation_Troubleshooting_Guide.md)**: 4인자 API 규칙, 바디 추적 로직, 서피스 커터 전략 등 상세 기록.

---

## 🚦 시작하기
1. SpaceClaim에서 `01_extractor/scdm_extractor.py`를 실행하여 기하 정보를 추출합니다.
2. 로컬 환경에서 `python main_run.py [기기이름]`를 실행하여 최적화된 분할 스크립트를 생성합니다.
3. 생성된 `04_scripts/xxxx_scdm_script.py`를 다시 SpaceClaim에서 실행하여 자동 분할을 완료합니다.
