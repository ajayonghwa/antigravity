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

## 7. 고유 ID 부여 전략 (Rename-on-Extract)

### 🚩 문제: 복수 컴포넌트 내 동일 이름 바디 충돌
여러 컴포넌트에 `Solid`라는 이름의 바디가 중복해서 존재할 경우, 이름 기반 추적 로직이 엉뚱한 바디를 자르는 현상이 발생할 수 있습니다.

*   **해결 (ID 기반 강제 명명)**:
    - **추출(Extract) 단계**에서 모든 대상 바디의 이름을 `AUTO_BODY_0`, `AUTO_BODY_1`과 같이 유니크한 ID로 변경합니다.
    - 원래 이름은 메타데이터(`original_name`)로만 보관합니다.
*   **이점**:
    - **추적 무결성**: `startswith("AUTO_BODY_0")`는 오직 해당 ID를 가진 바디와 그 조각들만 매칭함을 100% 보장합니다.
    - **ID 체계 확립**: 이후 해석 자동화 단계에서도 이 고유 ID를 키값으로 활용할 수 있습니다.

---

## 8. 동적 커터 크기 결정 (Dynamic Bounding Box)

*   **문제**: 모델의 크기가 매우 클 경우 고정된 반경(예: 5m)의 커터 서피스가 모델을 완전히 가로지르지 못해 분할에 실패할 수 있습니다.
*   **해결**: `GetRootPart().Range`를 사용하여 모델 전체의 대각선 길이를 계산하고, 이의 1.5배 이상을 커터 반경으로 설정하여 어떤 크기의 모델에서도 분할이 성공하도록 보장합니다.

---

## 9. 이름 충돌 3단계 방어 체계 (v3.1)

*   **문제**: `AUTO_BODY_X` 형태의 이름 변경이 모종의 이유(SCDM 내부 락 등)로 실패할 경우 분할 파이프라인이 붕괴됨.
*   **해결**:
    1.  **Rename**: `body.Name = "AUTO_BODY_X"` (최우선)
    2.  **Attribute**: 실패 시 `body.SetTextAttribute("AutoDecomp.UniqueID", "AUTO_BODY_X")`로 백업.
    3.  **Fingerprint**: 모두 실패 시 `Volume`과 Bounding Box Center 좌표를 조합한 해시값을 식별자로 사용.

---

## 10. 메쉬 품질 기반 분할 판단 (WHR) (v3.1)

*   **문제**: 너무 벽에 가까운 구멍에 O-Grid를 억지로 적용하면 벽 쪽 셀(Cell)이 극도로 찌그러짐.
*   **해결**: Wall-to-Hole Ratio (WHR) 개념 도입.
    *   WHR < 1.0: O-Grid 생략 (또는 반원형 C-Grid 적용)
    *   1.0 <= WHR <= 6.0: 정상 O-Grid 적용
    *   WHR > 6.0: O-Grid 생략 (자유 메쉬로 충분히 해소 가능)
    *   단, **직경 50mm 이상 대형 구멍**은 WHR에 무관하게 항상 O-Grid 적용.

---

## 11. 7대 실무 형상 맞춤형 전략 (v3.1)

*   **문제**: 단일 축 기반의 O-Grid/Sector/Axial 만으로는 다공판, 엘보우 등 실무 형상 대응 불가.
*   **해결**: 7가지 분류(Classification) 도입.
    1.  **다공판 (Perforated Plate)**: H-Grid Matrix + O-Grid
    2.  **단차 원판 (Stepped Disk)**: 직경 변화점 기반 최적화 Axial + Sector
    3.  **엘보우 (Elbow)**: Toroidal 면 감지 후 Sweep Path Cut (횡단면 분할)
    4.  **크로스 홀 (Cross Hole)**: 주 원통 Sector 각도를 45도 비틀어 측면 구멍 회피 + O-Grid
    5.  **얇은 원통 (Thin-walled Cylinder)**: O-Grid 생략 + Sector 분할
    6.  **볼트/와셔 (Fastener)**: Bounding Box 기준 극소형 부품 복잡 분할 생략
    7.  **튀어나온 블록 (Protruding Boss)**: 밑면 평면 기반 사전 분할 (Boss Separation)

---

## 12. 패턴 바디 수동 독립화 (v3.1)

*   **문제**: 인스턴스(Pattern)로 묶인 여러 바디 중 하나를 자르면, 연동된 다른 바디들이 엉뚱한 위치에서 함께 잘림.
*   **해결**: `Component.MakeIndependent()` API가 직접 노출되지 않는 환경을 우회하기 위해, 스크립트 실행 최우선 단계에서 `body.Shape.Copy()`를 통해 기하를 복사하고 `DesignBody.Create()`로 새 독립 바디를 만든 후 원본을 `Delete()` 하는 수동 독립화 함수(`make_all_bodies_independent`) 적용.

---

## ⚠️ 주의사항 (개발 시 참고)
- **단위(Unit)**: SCDM API 내부 단위는 항상 **Meter**입니다. Planner에서 계산 시 0.001을 곱하는 것을 잊지 마세요.
- **Selection**: 명령을 내릴 때마다 `Selection.Create()`로 감싸주는 것이 API 안정성에 좋습니다.
- **Delete**: 커터로 사용한 서피스 바디는 분할 직후 `Delete()`하여 모델을 깨끗하게 유지해야 합니다.
