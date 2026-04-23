# SpaceClaim API Reference (Verified by User Record)

이 문서는 사용자님께서 직접 SCDM에서 Record 기능을 통해 검증하신 성공 구문들을 정리한 참조 파일입니다. 
향후 모든 스크립트 생성 시 이 구문을 최우선으로 적용합니다.

## 1. 커터 생성 (ExtrudeEdges)
원통형 커터를 만들기 위해 커브의 엣지를 압출할 때 사용하는 정석 구문입니다.

```python
# 성공 구문 예시
selection = Selection.Create(dc.Edges[0])
options = ExtrudeEdgeOptions()
# 인자 순서: (선택 영역, 방향 벡터/평면, 압출 거리, 옵션, 정보객체)
result = ExtrudeEdges.Execute(selection, direction, MM(10000), options, None)
```

## 2. 솔리드 분할 (SplitBody)
생성된 커터를 도구로 사용하여 원본 솔리드를 자를 때 사용하는 정석 구문입니다.

```python
# 성공 구문 예시
selection = Selection.Create(targets) # 자를 대상 솔리드
toolFaces = Selection.Create(new_b.Faces[0]) # 도구가 될 커터의 면
# 인자 순서: (대상 솔리드, 커터 면, 병합 여부, 정보객체)
result = SplitBody.ByCutter(selection, toolFaces, True, None)
```

## 3. 네임스페이스 충돌 방지 (Critical)
'Create of namespace is readonly' 에러를 방지하기 위한 객체 접근 원칙입니다.

*   **Selection**: 반드시 `SpaceClaim.Api.V22.Scripting.Selection` 전체 경로를 경유하거나, 해당 클래스를 변수로 받아 `Create`를 호출해야 함.
*   **Point/Direction**: `SpaceClaim.Api.V22.Geometry.Point.Create` 형식을 사용하거나, 전역 스코프가 확실할 때만 `Point.Create` 사용.

## 4. 좌표계 및 정렬 (Orientation)
O-Grid 및 단면 분할 시 커터가 90도 회전하는 것을 방지하는 정렬 원칙입니다.

*   **Frame**: `Frame.Create(origin, normal)` 호출 시 `normal`이 프레임의 Z축(법선)이 됨을 보장.
*   **Circle**: `Circle.Create(temp_frame, radius)`를 통해 프레임의 XY 평면에 원을 생성하여 법선 방향을 일치시킴.
