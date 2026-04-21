import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(pdf_path, password=None):
    """
    Extracts text from a PDF file. 
    Handles basic encryption if a password is provided.
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        if doc.is_encrypted:
            if password:
                if not doc.authenticate(password):
                    return f"Error: Authentication failed for {pdf_path.name}"
            else:
                return f"Error: {pdf_path.name} is encrypted. Please provide a password."
        
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"

def load_all_references(ref_dir, password=None):
    """
    Loads all PDF and TXT files from the references directory.
    """
    p = Path(ref_dir)
    combined_text = ""
    for file in p.glob("*"):
        if file.suffix.lower() == ".pdf":
            combined_text += f"\n--- Reference: {file.name} ---\n"
            combined_text += extract_text_from_pdf(file, password)
        elif file.suffix.lower() == ".txt":
            combined_text += f"\n--- Reference: {file.name} ---\n"
            combined_text += file.read_text(encoding="utf-8")
    return combined_text
