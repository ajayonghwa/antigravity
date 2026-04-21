import json
import os
from pathlib import Path
from main import DocAssistant
from pdf_utils import extract_text_from_pdf

class QuickDocAssistant(DocAssistant):
    def step1_generate_outline(self, topic):
        print(f"\n[Quick Test] '{topic}' 주제로 짧은 개요를 생성합니다...")
        # test_ref.txt만 명시적으로 읽기
        ref_path = self.paths["refs"] / "test_ref.txt"
        refs = ref_path.read_text(encoding="utf-8") if ref_path.exists() else "No reference found."
        
        prompt = f"주제: {topic}\n\n참고 문헌:\n{refs}\n\n위 내용을 바탕으로 딱 2개의 섹션만 만들어주세요. 'Section X: 제목' 형식으로 작성하세요."
        system_prompt = "당신은 전문적인 문서 작성을 돕는 어시스턴트입니다. 아주 간결하게 한국어로 답변하세요."
        
        outline = self.client.generate(prompt, system_prompt)
        outline_path = self.paths["content"] / "outline.md"
        outline_path.write_text(outline, encoding="utf-8")
        print(f"개요 생성 완료 (2개 섹션 제한).")
        return outline

    def step2_quick_draft(self):
        outline_path = self.paths["content"] / "outline.md"
        outline_text = outline_path.read_text(encoding="utf-8")
        sections = [line for line in outline_text.split("\n") if "Section" in line]
        
        drafts = {}
        print("\n[Quick Test] 초안을 자동으로 짧게 생성합니다...")
        for section in sections:
            mock_input = f"{section}에 대한 핵심 트렌드 위주로 한 문장만 작성해줘."
            refined_text = self.client.generate(mock_input, "당신은 요약 전문가입니다.")
            drafts[section] = refined_text
            print(f"Drafted: {section}")

        with open(self.paths["content"] / "drafts.json", "w", encoding="utf-8") as f:
            json.dump(drafts, f, ensure_ascii=False, indent=2)

def run_quick_test():
    assistant = QuickDocAssistant()
    topic = "2026 AI 기술 요약"
    
    assistant.step1_generate_outline(topic)
    assistant.step2_quick_draft()
    assistant.step3_assemble("Quick_Test_Result")
    print("\n[완료] output/Quick_Test_Result.docx 파일을 확인하세요.")

if __name__ == "__main__":
    run_quick_test()
