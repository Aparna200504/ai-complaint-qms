from pathlib import Path
from email import policy
from email.parser import BytesParser

from PyPDF2 import PdfReader
from docx import Document


def extract_txt(file_path: str) -> str:
    """Extract text from a TXT file."""
    return Path(file_path).read_text(encoding="utf-8")


def extract_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)

    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_eml(file_path: str) -> str:
    """Extract the readable body from an EML email."""
    with open(file_path, "rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    body_parts = []

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_content()
                if content:
                    body_parts.append(content)
    else:
        if message.get_content_type() == "text/plain":
            body_parts.append(message.get_content())

    return "\n".join(body_parts)


def extract_document(file_path: str) -> str:
    """
    Extract text based on the document's file extension.
    Supported formats: PDF, DOCX, TXT, EML.
    """
    extension = Path(file_path).suffix.lower()

    extractors = {
        ".txt": extract_txt,
        ".pdf": extract_pdf,
        ".docx": extract_docx,
        ".eml": extract_eml,
    }

    extractor = extractors.get(extension)

    if not extractor:
        supported = ", ".join(extractors.keys())
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Supported formats: {supported}"
        )

    return extractor(file_path)