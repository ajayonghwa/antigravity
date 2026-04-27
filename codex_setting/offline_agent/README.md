# 오프라인 ANSYS 에이전트: 문서 인덱스/검색 (PoC v1)

목표: 에어갭 Windows 11에서 **ANSYS PDF + SpaceClaim CHM + (선택) pyansys 문서**를 로컬 인덱스로 만들고, 코드 생성 시 “근거 조각”을 뽑아 쓰게 한다.

## 폴더 구조(고정)

아래 3개 폴더만 있으면 된다. 파일명은 마음대로 바꿔도 된다.

```
<DOCS_ROOT>/
  ansys/        # *.pdf (OCR 텍스트) 또는 *.txt(사전 추출 텍스트)
  spaceclaim/   # *.chm
               # (CHM이 아직 없으면) spaceclaim_api_summary 같은 *.md/*.txt를 여기에 넣어도 됨
  pyansys/      # (선택) HTML 미러 또는 텍스트 자료
```

## (권장) 가상환경

에어갭 머신의 Python 3.10에서:

```bat
py -3.10 -m venv .venv
.venv\Scripts\activate
```

PDF 텍스트 추출을 파이썬만으로 하고 싶으면 `pypdf`가 필요할 수 있다.
(에어갭이면 wheel로 반입해서 설치)

## 인덱스 생성

```bat
python offline_agent\index\build_index.py ^
  --docs-root "D:\docs" ^
  --out "D:\index\docs_index.sqlite"
```

또는 배치 스크립트:

```bat
offline_agent\run_build_index.bat "D:\docs" "D:\index\docs_index.sqlite"
```

## (선택) pyansys docstring 덤프(버전 일치 근거)

웹 매뉴얼이 너무 많으면, “설치된 패키지 자체의 docstring/type 정보”를 인덱싱하는 게 가장 안전하다.
오프라인 머신에서:

```bat
python offline_agent\index\dump_docstrings.py ^
  --modules "ansys.dpf.core,ansys.mapdl.core" ^
  --out "D:\docs\pyansys\pyansys_docstrings.jsonl"
```

그 다음 `build_index.py`를 다시 실행하면 `pyansys_docstring` 소스로 같이 검색된다.

## 검색(근거 조각 뽑기)

```bat
python offline_agent\index\search.py --db "D:\index\docs_index.sqlite" --q "PRXY poisson"
```

또는 배치 스크립트:

```bat
offline_agent\run_search.bat "D:\index\docs_index.sqlite" "PRXY poisson"
```

출력되는 `chunk_id`가 “근거 ID”다. 코드 생성 프롬프트에 이 ID를 포함시키고,
수정 루프에서는 “에러 로그 + 실패 코드 + 근거 ID”를 같이 준다.

## 로컬 LLM과 연결(실전 사용법)

핵심은 “인덱스 → 근거 조각 → LLM 프롬프트”를 한 번 더 이어주는 것이다.

### 가장 단순한 연결(권장 v1)

1) 코딩 작업이 생기면 먼저 근거를 뽑는다:

```bat
py -3.10 offline_agent\rag\get_context.py --db "D:\index\docs_index.sqlite" --q "MassProperties GetInertiaTensor" --k 6
```

2) 출력된 `# SOURCES` 블록을 그대로 에이전트(Cline/Continue 등) 프롬프트에 붙여넣고,
   “근거 없는 API 호출 금지” 규율로 코드를 생성하게 한다.

이 방식은 에어갭에서 가장 견고하다. 에이전트 플러그인에 “도구 호출” 연동이 없어도 동작한다.

### 조금 더 자동화(선택)

- 에이전트가 터미널 명령을 실행할 수 있다면(대부분 가능):
  - 에이전트에게 “코드 작성 전에 `get_context.py`를 실행하고 결과만 사용하라”는 룰을 주면 된다.

프롬프트 템플릿은 여기:
- `offline_agent/rag/agent_prompt_template.md`

## 처음에 봐야 할 문서(추천 순서)

내용이 많아도 아래만 먼저 보면 된다:

1) `offline_agent/README.md` (이 문서)
2) `continue_system_prompt_offline_ansys.md` (Continue 규율, 가장 중요)
3) `spaceclaim_script_prompt.md` (SpaceClaim 스크립트 생성 입력/규율)
4) `ANSYS_오프라인_코드생성_루틴.md` (전체 워크플로우 요약)
5) `beam_tuning/README.md` (빔/쉘 초안 → 분할/노드추가 → 튜닝 흐름)
6) `오프라인-ANSYS-에이전트-구현계획-20260427.md` (PoC 실행 계획)
