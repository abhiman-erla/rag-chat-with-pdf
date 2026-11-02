from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Read all pages from a PDF and combine them into one text string."""
    reader = PdfReader(str(pdf_path))
    page_text = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        cleaned = text.strip()
        if cleaned:
            page_text.append(f"[Page {index}]\n{cleaned}")

    return "\n\n".join(page_text)
