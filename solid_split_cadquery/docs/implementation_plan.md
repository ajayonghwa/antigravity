# Solid Split CadQuery 구현 계획서

이 프로젝트는 SpaceClaim(SCDM)의 솔리드 분할 로직을 **CadQuery**를 사용하는 순수 파이썬 환경으로 마이그레이션하는 것을 목표로 합니다. 이를 통해 SpaceClaim 설치 없이도 기하 형상 분할 작업이 가능해집니다.

## 사용자 검토 필요 사항

> [!IMPORTANT]
> 현재 계획은 SCDM 프로젝트의 **7가지 분할 전략**(O-Grid, H-Grid, Sector 등)을 CadQuery로 이식하는 것을 가정하고 있습니다. 이 범위가 맞는지 확인 부탁드립니다.

> [!NOTE]
> CadQuery(v2.7.0)가 이미 설치되어 있으므로, 환경 구축보다는 핵심 분할 로직 구현에 집중하겠습니다.

## 주요 질문

1. **입력/출력**: 도구가 주로 STEP 파일을 읽어 분할하는 방식이어야 할까요, 아니면 파라미터 기반으로 새로운 형상을 생성하며 분할하는 방식이어야 할까요?
2. **전략 이식**: 7가지 전략을 즉시 모두 구현할까요, 아니면 가장 일반적인 O-Grid와 평면 분할(Planar Split)부터 시작할까요?
3. **시각화**: 결과 확인은 어떻게 하고 싶으신가요? `.step` 파일로 내보내 외부 뷰어에서 확인하는 것으로 충분할까요?
4. **통합**: 기존 `validator` 및 `optimizer` 폴더에 있는 로직들을 이 새 폴더로 옮겨 하나로 통합할까요?

## 변경 사항 제안

### 프로젝트 구조 [신규]

`solid_split_cadquery/` 내에 기하 추출, 분류 및 분할 로직을 분리하여 모듈식 구조를 구축합니다.

#### [신규] [main.py](file:///Users/yonghwaheo/Documents/antigravity/solid_split_cadquery/main.py)
분할 파이프라인의 엔트리 포인트입니다.

#### [신규] [classifier.py](file:///Users/yonghwaheo/Documents/antigravity/solid_split_cadquery/core/classifier.py)
STEP 기하 형상을 분석하여(`topology_auditor.py` 로직 활용) 어떤 전략을 적용할지 결정합니다.

#### [신규] [splitter.py](file:///Users/yonghwaheo/Documents/antigravity/solid_split_cadquery/core/splitter.py)
CadQuery의 `.split()` 및 `.cut()` 메서드를 사용하여 실제 분할 작업(O-Grid, 평면 분할 등)을 수행합니다.

#### [신규] [geometry_utils.py](file:///Users/yonghwaheo/Documents/antigravity/solid_split_cadquery/core/geometry_utils.py)
벡터 연산 및 바운딩 박스 계산을 위한 헬퍼 함수들을 포함합니다.

---

### 마이그레이션 및 정리

#### [신규] [README.md](file:///Users/yonghwaheo/Documents/antigravity/solid_split_cadquery/README.md)
새로운 CadQuery 기반 워크플로우와 SCDM 의존성 대체 방법을 문서화합니다.

## 검증 계획

### 자동 테스트
- `examples/test_splits.py` 테스트 스크립트를 작성하여 기본 실린더를 생성하고 O-Grid 분할을 수행합니다.
- 분할 후 결과 바디의 개수를 확인합니다.

### 수동 검증
- 분할된 형상을 STEP 파일로 내보내고, 사용자가 CAD 뷰어에서 결과를 확인하도록 요청합니다.
