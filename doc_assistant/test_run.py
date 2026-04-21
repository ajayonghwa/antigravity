from main import DocAssistant
import json
import os

def auto_test():
    assistant = DocAssistant()
    
    # Step 1: 개요 생성
    print("--- Step 1: Outline Generation ---")
    assistant.step1_generate_outline("2026 AI 기술 트렌드")
    
    # Step 2: 대화형 초안 작성 시뮬레이션
    print("\n--- Step 2: Draft Simulation ---")
    outline_path = assistant.paths["content"] / "outline.md"
    outline_text = outline_path.read_text(encoding="utf-8")
    sections = [line for line in outline_text.split("\n") if "Section" in line]
    
    drafts = {}
    for section in sections:
        # 가상의 사용자 입력
        mock_input = f"{section}에 대한 상세 기술적 분석과 시장 전망 데이터가 필요합니다. 특히 트렌드 변화에 주목해야 합니다."
        refining_prompt = f"섹션: {section}\n사용자 입력: {mock_input}\n\n이 내용을 바탕으로 공식적인 문서에 적합한 문단으로 다듬어주세요."
        refined_text = assistant.client.generate(refining_prompt, "당신은 전문 에디터입니다.")
        drafts[section] = refined_text
        print(f"Drafted: {section}")

    with open(assistant.paths["content"] / "drafts.json", "w", encoding="utf-8") as f:
        json.dump(drafts, f, ensure_ascii=False, indent=2)

    # Step 3: 최종 문서 조립
    print("\n--- Step 3: Assembling Document ---")
    assistant.step3_assemble_docx("Test_Result.docx")

if __name__ == "__main__":
    auto_test()
