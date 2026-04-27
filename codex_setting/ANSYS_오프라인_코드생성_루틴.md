# ANSYS/DPF/APDL 오프라인 코드생성 루틴 (작은 로컬 LLM용)

목표: gemma4:e4b-it-Q4 같은 작은 로컬 모델로도 **오류 가능성이 낮은 코드 초안**을 만들고, **에러 로그 기반 수정**을 반복 가능하게 만든다.

핵심 원칙 3개:

1. **근거 없는 호출 금지**: 매뉴얼/레퍼런스 발췌(페이지/토픽) 또는 로컬 docstring 근거가 없는 API/키워드는 쓰지 않는다.
2. **스켈레톤 고정**: APDL/DPF 코드는 “정석 템플릿”을 먼저 깔고, 채워 넣는 방식으로 생성 공간을 좁힌다.
3. **가드레일은 규칙으로**: 자주 틀리는 건 LLM이 아니라 룰(검사/치환)로 막는다.

---

## 1) 코드 생성 요청 템플릿 (사용자 → 에이전트)

아래 형식으로 요청하면, 에이전트가 “근거 발췌 → 코드 초안” 순서로 작업하기 쉬워진다.

### A. SpaceClaim(영역 질량/관성/질량중심 + 형상 특징)

- 목적:
- SpaceClaim 버전:
- 입력: 모델 파일 경로/이름(또는 이미 열려있는 상태인지)
- 선택 영역 정의 방식:
  - (기본) Named selection / Face/Body ID / selection rule
  - (추가) 좌표 범위로 “잘라내서 선택”(복수 구간 지원)
    - v1: 1축(x/y/z 중 하나) 범위만 지원
    - 예: `z=100~250mm`
    - 예: 구간 여러 개면 `segment_id=1..N`으로 각각 별도 추출
- 원하는 출력:
  - 질량/관성/질량중심: (좌표계는 global? local?)
  - 형상 특징: (예: cylinder ID/OD, disk OD/thickness)
- 출력 포맷: CSV / JSON / 텍스트

SpaceClaim 스크립트 생성 템플릿/프롬프트:
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/spaceclaim_script_prompt.md`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/spaceclaim_extract_template.py`

### B. DPF 후처리(변위/반력/응력 + 응력선형화 준비)

- 목적:
- 입력 결과파일: `*.rst` 경로
- 해석 유형: static / modal / harmonic …
- 관심 단계/모드: (예: mode 1~6)
- 필요한 결과:
  - displacement / velocity / acceleration (가능하면 명시)
  - reaction force (node set / boundary name)
  - stress (성분/좌표계)
- 응력선형화:
  - SCL 정의(가능하면): 두 점(시작/끝) + 두께 방향
  - 최소 목표: “SCL 위 응력 샘플 CSV 저장”까지인지, “선형화 계산”까지인지

DPF 골격 템플릿:
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/dpf_postprocess_template.py`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/dpf_scoping_example.json`

### C. APDL(모드해석, 재료/단면/요소, 빔/쉘 모델)

- 목적: (modal tuning 포함 여부)
- 요소 타입: beam / shell (가능하면 명시)
- 재료:
  - E, density, nu(포아송비) 등
  - 단, APDL 키워드로 매핑 요구: 예) 포아송비는 `PRXY`
- 해석:
  - modal(모드해석)인지 반드시 명시
  - 원하는 모드 수/주파수 범위

빔/쉘 모델 생성 + 튜닝 입력 템플릿:
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/segments_template.csv`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/targets_template.csv`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/connectors_template.csv`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/nodes_template.csv`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/beams_template.csv`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/run_tuning.py`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/add_nodes.py`
- `/Users/yonghwaheo/Documents/antigravity/codex_setting/beam_tuning/split_beams.py`

---

## 2) 에러 수정 요청 템플릿 (사용자 → 에이전트)

수정은 “추측”이 아니라 “근거 교체”로 가야 한다. 아래 3가지를 항상 같이 준다.

1) **에러 로그 전문**(Traceback / 메시지)  
2) **실패한 코드 블록**(가능하면 파일 전체)  
3) **이 코드가 참조한 근거 ID**(문서 발췌 페이지/토픽, 또는 docstring 경로)

---

## 3) 최소 가드레일(룰) 2개: 지금 바로 효과 나는 것

### A. 포아송비 키워드 고정

- 사용자 입력이 `nu`든 `poisson`이든, APDL 출력 코드는 **항상 `PRXY`**를 사용한다.
- 근거(매뉴얼 발췌/로컬 docstring)에 `PRXY`가 등장하지 않으면:
  - “근거 부족”으로 생성 중단하고, `PRXY`가 있는 섹션을 재검색하도록 한다.

### B. 모드해석 vs 정적해석 혼동 방지

- 사용자 요청이 “모드해석(modal)”이면, APDL 출력에 다음이 포함되어야 한다:
  - `ANTYPE,MODAL` (또는 조직 표준 템플릿의 모달 고정 토큰)
- 동시에 `STATIC` 계열 토큰(또는 정적 전용 설정)이 섞이면:
  - 경고 후 “모달 템플릿”으로 다시 생성한다.

---

## 4) 산출물(파일) 표준

작은 모델은 “정확한 결과 형식”이 있어야 실수가 줄어든다.

- APDL: `*.mac` 또는 `*.inp` + 상단에 “목적/가정/근거” 헤더(짧게)
- DPF: `postprocess_dpf.py` + 출력 CSV/PNG 경로 고정
- SpaceClaim: `spaceclaim_extract.py`(환경에 맞는 스크립트) + 결과 CSV 고정
