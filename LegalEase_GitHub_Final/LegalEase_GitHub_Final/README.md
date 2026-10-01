# LegalEase — AI-Powered Legal Document Generator

LegalEase is a Python-based legal document generator built with **Streamlit** for the frontend, **FastAPI** for the backend, and optional **Google Gemini** generation. It supports editable previews and exports to TXT, DOCX, and PDF.

## Project structure

```text
LegalEase/
├── app.py                         # Streamlit website
├── main.py                        # FastAPI application
├── routes.py                      # /generate API route
├── formatting.py                  # Preview, DOCX and PDF formatting
├── start.py                       # Starts backend + frontend together
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .gitignore
└── ai_core/
    ├── __init__.py
    └── gemini_generator.py        # Gemini integration + local fallback
```

## Run locally

### 1. Install Python
Use Python 3.10+.

### 2. Open a terminal in this folder

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini (optional)

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Do **not** commit `.env` to GitHub. It is excluded by `.gitignore`.

### 5. Start the complete website

```bash
python start.py
```

Then open the Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

### Alternative: start backend and frontend separately

Terminal 1:

```bash
uvicorn main:app --reload
```

Terminal 2:

```bash
streamlit run app.py
```

## Features

- Legal document type input
- Parties involved input
- Semicolon-separated terms and conditions
- Effective date input
- AI-assisted document generation with Gemini
- Local fallback generation when Gemini is not configured
- Dark themed scrollable document preview
- Editable generated document
- TXT export
- DOCX export with LegalEase branding and footer
- PDF export with LegalEase branding and footer
- FastAPI `/generate` endpoint

## GitHub upload

1. Create a new GitHub repository.
2. Extract/download this project folder.
3. Upload the **contents of this folder** to the GitHub repository root.
4. Make sure `.env` is **not** uploaded.
5. Commit the files.

The project is designed to run locally after cloning with the installation and run commands above.

## API

### `GET /`
Health check.

### `POST /generate`
Example JSON body:

```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
  "dates": "April 10, 2025"
}
```

## Note

This project generates document drafts and is not a substitute for review by a qualified legal professional.
