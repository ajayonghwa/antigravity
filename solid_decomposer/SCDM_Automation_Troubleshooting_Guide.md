# SCDM Geometry Decomposition: Troubleshooting & Engineering Guide

이 문서는 SpaceClaim(SCDM) 기하 분할 자동화 파이프라인을 구축하며 발견한 핵심 문제점들과 이를 해결하기 위해 적용된 기술적 논리를 상세히 기록합니다. 대화 기록이 유실되거나 코드를 리팩토링할 때 반드시 참고해야 하는 지침서입니다.

---

## 1. API 참조 및 네임스페이스 (The Loading Mystery)

### 🚩 문제: `name 'Commands' is not defined`
SCDM 스크립트 창에서 직접 실행할 때와 외부에서 생성된 스크립트를 실행할 때의 환경 차이로 인해 발생하는 에러입니다.

*   **원인**: IronPython 환경에서 .NET 어셈블리(`SpaceClaim.Api.V19`)가 명시적으로 로드되지 않아 관련 클래스를 찾지 못함.
*   **해결**: 
    - `clr.AddReference("SpaceClaim.Api.V19")`를 반드시 임포트 전에 실행.
    - 버전 호환성을 위해 V17~V22까지 루프를 돌며 동적으로 참조를 추가하는 `initialize_api()` 로직 구현.
    - `from ... import *`를 사용하여 전역 네임스페이스에 클래스를 풀어놓음으로써 `Commands.` 접두사 없이도 호출 가능하게 함.

---

## 2. 명령어 시그니처 (The 4-Argument Rule)

### 🚩 문제: `'type' object has no attribute 'Execute'` 또는 `'ExtrudeEdgesResult' has no attribute 'CreatedBodies'`
동작은 기록되는데 실행 시 에러가 나거나, 결과값을 읽지 못하는 현상입니다.

*   **원인**: SCDM API 버전(특히 사용자 환경)에 따라 명령어가 요구하는 인자 개수가 다름. 보통 3개 인자로도 작동하지만, 안정적인 실행을 위해서는 **`CommandInfo` (보통 None)**를 포함한 4개 또는 5개 인자가 필수적임.
*   **핵심 해결 코드**:
    ```python
    # SplitBody의 경우 반드시 4개 인자 (Target, Cutter, Boolean, Info)
    SplitBody.ByCutter(target_sel, cutter_sel, True, None)
    
    # ExtrudeEdges의 경우 4개 또는 5개 인자 시도
    try:
        ExtrudeEdges.Execute(sel, dist, options, None) # 4인자
    except:
        ExtrudeEdges.Execute(sel, dir, dist, options, None) # 5인자
    ```

---

## 3. 바디 추적 로직 (The Fragment Problem)

### 🚩 문제: 첫 번째 분할 후 다음 분할이 적용되지 않음 (1/2 조각만 남는 현상)
하나의 솔리드를 자르면 이름이 바뀌어 버려 다음 명령어가 대상을 찾지 못하는 문제입니다.

*   **원인**: `Plate`를 자르면 `Plate`와 `Plate (1)`(또는 `Plate_1`)이 생기는데, 스크립트가 원래 이름인 `Plate`만 찾으려 하기 때문.
*   **해결 (저인망식 추적)**: 
    - `get_matching_bodies` 함수를 만들어 `startswith(target_base)` 로직 적용.
    - 원래 이름으로 시작하는 모든 조각을 리스트로 수집하여 루프를 돌며 각각에 명령을 수행함.

---

## 4. 커터 생성 전략 (Surface vs. Hollow Cylinder)

### 🚩 문제: `SECTOR`(90도) 분할 시 `unable to split` 에러 발생
평면으로 잘라야 하는데 O-grid 방식을 그대로 쓰려다 발생한 기하학적 오류입니다.

*   **원인**: `ExtrudeEdges`를 원형 커브에 적용하면 "속이 빈 얇은 원통"이 생성됨. 이를 평면 분할 커터로 쓰면 면이 아닌 엣지만 닿아 분할에 실패함.
*   **해결**:
    - **O-GRID**: 원통 면이 필요하므로 `ExtrudeEdges` 사용.
    - **SECTOR / AXIAL**: 원을 그린 뒤 **`Fill.Execute`**를 사용하여 "속이 꽉 찬 평면 쟁반(Surface)"을 생성. 이 면(Face)을 커터로 사용해야 완벽하게 잘림.

---

## 5. 실행 순서의 논리 (Partition First, Detail Later)

### 🚩 설계 원칙: 분할(Partition) → O-Grid
순서가 바뀌면 기하학적 간섭으로 인해 연산이 꼬입니다.

1.  **SECTOR 분할 (최우선)**: 원판을 먼저 4등분함. 가장 깔끔한 상태에서 큰 칼질을 먼저 함.
2.  **AXIAL 분할**: 층을 나눔.
3.  **OGRID 분할 (마지막)**: 이미 나뉜 각 조각 안에서 구멍들을 처리함.

---

## 6. O-Grid 필터링 및 안정화 기술

*   **Peripheral Filtering**: 바디 외곽(반지름 75% 이상 지점)에 있는 구멍은 메쉬 품질 저하를 막기 위해 O-Grid 대상에서 제외 (`strategy_planner.py`의 `dist_from_main` 로직).
*   **Interference Avoidance**: 구멍끼리 너무 가까우면 O-Grid 커터가 서로 겹침. 이때는 `core_offset`을 강제로 줄여 간섭을 회피함.
*   **Diffing Logic (무적 로직)**: 명령어 결과 객체(`Result`)의 속성명이 버전마다 다르므로(`CreatedBodies` vs `CreatedObjects`), 명령 실행 전/후의 바디 목록 차이를 비교하여 새로 생긴 커터를 100% 잡아냄.

---

## ⚠️ 주의사항 (개발 시 참고)
- **단위(Unit)**: SCDM API 내부 단위는 항상 **Meter**입니다. Planner에서 계산 시 0.001을 곱하는 것을 잊지 마세요.
- **Selection**: 명령을 내릴 때마다 `Selection.Create()`로 감싸주는 것이 API 안정성에 좋습니다.
- **Delete**: 커터로 사용한 서피스 바디는 분할 직후 `Delete()`하여 모델을 깨끗하게 유지해야 합니다.
