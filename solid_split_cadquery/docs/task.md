# 작업 목록: solid_split_cadquery

- [x] 프로젝트 구조 및 문서화 초기화
    - [x] 디렉토리 구조 생성 (`input`, `output`, `core`, `examples`)
    - [x] `requirements.txt` 생성
    - [x] `README.md` 생성
- [x] 핵심 로직 구현
    - [x] `core/geometry_utils.py` 구현 (벡터 연산, BBox 헬퍼)
    - [x] `core/classifier.py` 구현 (특징 식별, 법선 벡터 분석, 주축 감지)
    - [x] `core/splitter.py` 구현 (O-Grid, 평면, 섹터(4분할), H-Grid 분할)
- [x] 통합 및 메인 스크립트
    - [x] `main.py` 구현 (CLI 및 오케스트레이터)
- [x] 검증 및 예제
    - [x] `examples/demo_ogrid.py` 생성 및 테스트
    - [x] `examples/demo_advanced_splits.py` 생성 및 테스트 (Sector & H-Grid)
    - [x] `validator/data` 예제 대상 일괄 테스트 및 시각화 보고서 생성
    - [x] STEP 내보내기 기능 검증
