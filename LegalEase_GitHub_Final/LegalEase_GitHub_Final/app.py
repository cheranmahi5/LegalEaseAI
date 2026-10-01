import os
import requests
import streamlit as st
from dotenv import load_dotenv

from formatting import format_docx, format_pdf, sanitize_text, format_html_preview

load_dotenv()

st.set_page_config(page_title="LegalEase", page_icon="⚖", layout="centered")

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {padding-top:1rem; padding-bottom:2rem; max-width:1100px;}
.logo-wrap {text-align:center; margin-top:.2rem; margin-bottom:.2rem;}
.logo {font-family:Georgia,serif; font-size:2.25rem; font-weight:700; color:#111827; letter-spacing:-.04em;}
.logo span {font-size:2rem; margin-right:.25rem;}
.hero-title {text-align:center; font-size:1.55rem; font-weight:500; margin:.25rem 0 1.4rem; color:#333;}
.field-label {font-weight:650; margin-top:.25rem; margin-bottom:.2rem; color:#222;}
.preview-box {background:#0e111a; border-radius:4px; padding:1.05rem; margin-top:.7rem;}
.preview-box .paper {background:#111827; color:#e7eaf0; border-radius:5px; padding:1.1rem; min-height:390px; max-height:530px; overflow:auto; font-family:Georgia,serif; line-height:1.55;}
.success {background:#0c4a2d; color:#c7f9dd; border-radius:4px; padding:.55rem .7rem; margin:.65rem 0; font-size:.9rem;}
.hint {color:#777; font-size:.82rem;}
[data-testid="stDownloadButton"] button {width:100%;}
</style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="logo-wrap"><div class="logo"><span>♎</span>LegalEase</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hero-title">AI Legal Document Generator</div>', unsafe_allow_html=True)

if "document" not in st.session_state:
    st.session_state.document = ""
if "editing" not in st.session_state:
    st.session_state.editing = False
if "message" not in st.session_state:
    st.session_state.message = ""

st.markdown('<div class="field-label">Document Type</div>', unsafe_allow_html=True)
document_type = st.text_input("Document Type", placeholder="e.g. Freelance Work Contract", label_visibility="collapsed")

st.markdown('<div class="field-label">Parties Involved</div>', unsafe_allow_html=True)
parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)", height=95, label_visibility="collapsed")

st.markdown('<div class="field-label">Terms & Conditions (Use semicolons for bullet points)</div>', unsafe_allow_html=True)
terms = st.text_area("Terms & Conditions", placeholder="Payment to be made within 30 days of invoice; The provider agrees to deliver work by the agreed deadline; Confidentiality must be maintained at all times; Either party may terminate with 15 days notice", height=120, label_visibility="collapsed")

st.markdown('<div class="field-label">Effective Date</div>', unsafe_allow_html=True)
dates = st.text_input("Effective Date", placeholder="April 10, 2025", label_visibility="collapsed")

if st.button("Generate Document", type="primary", use_container_width=True):
    payload = {"document_type": document_type or "Freelance Work Contract", "parties": parties, "terms": terms, "dates": dates}
    backend = os.getenv("LEGALEASE_BACKEND_URL", "http://localhost:8000/generate")
    try:
        response = requests.post(backend, json=payload, timeout=45)
        response.raise_for_status()
        st.session_state.document = sanitize_text(response.json().get("document", ""))
        st.session_state.message = "Document Generated Successfully!"
    except Exception:
        bullets = [x.strip() for x in terms.split(";") if x.strip()]
        st.session_state.document = sanitize_text(
            f"## {payload['document_type']}\n\n"
            f"Agreement made this {dates or '[Effective Date]'}\n\n"
            f"Between:\n\n{parties or '[Parties Involved]'}\n\n"
            "AGREEMENT\n\n"
            f"This {payload['document_type'].lower()} is entered into by the parties identified above.\n\n"
            "Terms and Conditions:\n" + "\n".join(f"- {b}" for b in bullets) +
            "\n\nIN WITNESS WHEREOF, the parties agree to the terms contained herein."
        )
        st.session_state.message = "Document Generated Successfully! (Local demonstration mode)"
    st.session_state.editing = False

if st.session_state.document:
    st.markdown(f'<div class="success">✓ {st.session_state.message}</div>', unsafe_allow_html=True)
    st.markdown('<div class="preview-box"><div class="paper">' + format_html_preview(st.session_state.document) + '</div></div>', unsafe_allow_html=True)

    if st.button("✎ Click to Edit Document", use_container_width=True):
        st.session_state.editing = True

    if st.session_state.editing:
        edited = st.text_area("Edit Document Below:", value=st.session_state.document, height=360)
        if st.button("Save Edits", use_container_width=True):
            st.session_state.document = sanitize_text(edited)
            st.session_state.editing = False
            st.rerun()

    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button("📄 Download as .TXT", st.session_state.document.encode("utf-8"), "LegalEase_Document.txt", "text/plain", use_container_width=True)
    with d2:
        st.download_button("📄 Download as .DOCX", format_docx(st.session_state.document, document_type or "Legal Document"), "LegalEase_Document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with d3:
        st.download_button("📕 Download as .PDF", format_pdf(st.session_state.document, document_type or "Legal Document"), "LegalEase_Document.pdf", "application/pdf", use_container_width=True)
