# Beam/Shell 모델 생성 + 모달 튜닝(초안) 워크플로우

목표:
- SpaceClaim에서 뽑은 영역별 질량/COG/관성(= COG 기준)을 기반으로 APDL 빔/쉘 모델을 만든다.
- 목표 고유진동수/방향별 유효질량을 입력으로 주고, 파라미터를 업데이트하며 튜닝한다.
- (고급, 옵션) 솔리드 모델의 모드형상과 비교해서 MAC까지 계산해 튜닝 신호로 사용한다.

## 입력 CSV (사용자가 채움)

1) `beam_tuning/segments_template.csv`
- SpaceClaim 추출 결과를 이 양식으로 맞춘다(빈칸 채우기 쉽게).
- 치수는 “값”뿐 아니라 “범위(min/max)”를 넣어서 튜닝 변수로 쓸 수 있게 한다.

2) `beam_tuning/targets_template.csv`
- 모드별 목표 주파수(Hz)와 방향별 유효질량 목표(또는 비율)를 넣는다.
- 가중치(weight)로 “어느 항목을 더 맞출지”를 조절한다.

- (선택) `beam_tuning/connectors_template.csv`
  - COMBIN14/39, MASS21, CE/CP/D 같은 “연결/구속/집중질량”을 템플릿 형태로 기록
  - v1에서는 APDL 문법을 지어내지 않기 위해 “구조/파라미터”만 표준화하고, 실제 APDL 명령은 사내 표준에 맞춰 채움

- (선택) `beam_tuning/nodes_template.csv`
  - 튜닝 이후에도 연계(조인트/구속/리모트포인트 등)를 위해 노드를 추가해야 할 때가 있음
  - 노드 번호 충돌을 피하려고 `node_id`를 **명시적으로** 적는다(이미 있는 번호와 겹치지 않게)
  - `shared_key`로 “영역 간 공유되어야 하는 노드”를 그룹화하고, `share_mode`로 shared/isolated를 표시한다

- (선택) `beam_tuning/beams_template.csv`
  - “빔 요소 중간에 노드 추가”는 노드만 추가하는 게 아니라, 빔을 여러 구간으로 **분할**해야 함
  - 이 CSV는 빔 라인(시작/끝 노드 + 좌표)과 삽입 위치(예: z=50)를 정의
  - `beam_tuning/split_beams.py`가 삽입 노드와 “새 연결쌍(new_pairs)”을 산출

## 실행(오프라인 PoC)

```bash
python beam_tuning/run_tuning.py --segments beam_tuning/segments_template.csv --targets beam_tuning/targets_template.csv --outdir out
```

연결/구속 CSV까지 포함:

```bash
python beam_tuning/run_tuning.py --segments beam_tuning/segments_template.csv --targets beam_tuning/targets_template.csv --connectors beam_tuning/connectors_template.csv --outdir out
```

튜닝 모드:
- 기본(주파수 + 방향별 유효질량): `--tuning-mode basic`
- 고급(+MAC): `--tuning-mode mac`

튜닝 이후 노드 추가(리튠 없이):

```bash
python beam_tuning/add_nodes.py --nodes beam_tuning/nodes_template.csv --out out/add_nodes.mac
```

`node_id`를 비워두고 “현재 모델 최대 노드 + 10” 규칙을 쓰려면:

```bash
python beam_tuning/add_nodes.py --nodes beam_tuning/nodes_template.csv --scan-apdl out/beam_model_template.mac --node-id-offset 10 --out out/add_nodes.mac
```

빔 중간 노드 삽입(빔 분할):

```bash
python beam_tuning/split_beams.py --beams beam_tuning/beams_template.csv --node-id-start auto --scan-apdl out/beam_model_template.mac --node-id-offset 10 --outdir out --emit-apdl
```

산출물:
- `out/inserted_nodes.csv`: 새로 만들어야 할 노드 목록
- `out/beam_splits.csv`: 각 빔이 어떤 노드쌍들로 분할되어야 하는지(new_pairs)
- `out/split_beams.mac`: 노드 생성 + “요소 분할” TODO를 담은 APDL 스켈레톤(사내 표준에 맞춰 채움)

기본 동작:
- APDL 입력/매크로 파일(템플릿)을 생성한다.
- 튜닝 루프는 환경에 따라:
  - `ansys.mapdl.core`가 있으면 파이썬에서 MAPDL 실행까지 연결
  - 없으면 “APDL 실행 → 결과 파일 경로를 다시 입력” 방식으로 단계별 진행

## MAC(고급, 옵션)

MAC을 자동화하려면 최소 2가지가 필요하다:
- 솔리드/빔 모델의 모드형상을 DPF로 읽을 수 있어야 함(`*.rst`)
- 두 모델의 DOF 매핑(같은 노드/같은 자유도 또는 매핑 테이블)

PoC v1에서는 “주파수 + 유효질량”을 먼저 맞추고, MAC은 v2로 올리는 걸 권장.
