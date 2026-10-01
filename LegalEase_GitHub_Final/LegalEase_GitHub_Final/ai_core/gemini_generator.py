import os

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-1.5-pro"
        self.model = None
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception:
                self.model = None

    def generate_document(self, document_type, parties, terms, dates):
        prompt = f"""Create a formal, structured legal document. Document type: {document_type}. Parties: {parties}. Effective date: {dates}. Terms and conditions: {terms}. Use clear headings, formal clauses, and preserve all supplied terms. Return document text only."""
        if self.model:
            response = self.model.generate_content(prompt)
            return response.text
        bullets = [x.strip() for x in terms.split(';') if x.strip()]
        return (f"{document_type.upper()}\n\nPARTIES\n{parties}\n\nEFFECTIVE DATE\n{dates}\n\n"
                f"TERMS & CONDITIONS\n" + "\n".join(f"- {x}" for x in bullets))
