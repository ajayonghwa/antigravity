# 오프라인 RAG 프롬프트 템플릿 (LLM 에이전트용)

아래는 Cline/Continue 같은 에이전트에게 그대로 주는 템플릿이다.

## 0) 로컬 LLM 사용

- 모델: `gemma4:e4b-it-Q4` (예: Ollama)
- 네트워크: OFF (에어갭)

## 1) 작업 시작 규율

1. 코드를 쓰기 전에 반드시 근거(SOURCES)를 가져온다.
2. 근거 없는 API/키워드/명령은 쓰지 않는다.
3. 출력 코드에는 사용한 `chunk_id`를 남긴다.

## 2) 근거 가져오기(사용자/에이전트가 실행)

Windows 예시:

```bat
py -3.10 offline_agent\rag\get_context.py --db D:\index\docs_index.sqlite --q "<QUERY>" --k 6
```

## 3) 본문 프롬프트 골격

```
TASK:
<내가 원하는 작업 설명>

CONSTRAINTS:
- offline
- no web
- use only SOURCES for API names/signatures

SOURCES:
<get_context.py 출력 붙여넣기>

OUTPUT:
- code only (or code + short usage)
- cite chunk_id list at end
```

