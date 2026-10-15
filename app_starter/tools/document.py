import base64
from pathlib import Path
from typing import Literal

from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field

SUPPORTED_EXTENSIONS: dict[str, Literal["docx", "pdf"]] = {
    ".docx": "docx",
    ".pdf": "pdf",
}


def _bytes_to_markdown(data: bytes, file_type: Literal["docx", "pdf"]) -> str:
    md = MarkItDown()
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(BytesIO(data), stream_info=stream_info)
    return result.text_content


def binary_document_to_markdown(
    binary_data: str = Field(
        description="Contents of the document file, base64-encoded"
    ),
    file_type: Literal["docx", "pdf"] = Field(
        description="Format of the document, given as its file extension without the dot"
    ),
) -> str:
    """Convert a binary document (DOCX or PDF) to markdown-formatted text.

    Decodes the base64-encoded file contents and returns the document's text
    as markdown, keeping structure such as headings, lists and tables where
    the source format allows. The file_type tells the converter how to
    interpret the decoded bytes, so it must match the document's real format.
    Raises an error if binary_data is not valid base64.

    When to use:
    - When you need to read or summarize the text of a Word or PDF document
    - When you need document content in a plain-text form for further processing
    - When you already have the file's contents rather than a path to it

    When not to use:
    - For a file on the server's disk; use document_path_to_markdown instead
    - For files that are already plain text or markdown; read them directly
    - For formats other than DOCX and PDF

    Examples:
    >>> binary_document_to_markdown("UEsDBBQABgAIAAAAIQ...", "docx")
    '# Report Title\\n\\nFirst paragraph of the report...'
    >>> binary_document_to_markdown("JVBERi0xLjcKJeLjz9MK...", "pdf")
    'Paper Title\\n\\nAbstract text...'
    """
    return _bytes_to_markdown(base64.b64decode(binary_data, validate=True), file_type)


def document_path_to_markdown(
    file_path: str = Field(
        description="Path to a .pdf or .docx file on the server's machine; an absolute path is safest"
    ),
) -> str:
    """Read a PDF or DOCX file from disk and convert it to markdown-formatted text.

    Reads the file at file_path and returns the document's text as markdown,
    keeping structure such as headings, lists and tables where the source
    format allows. The format is detected from the file extension (.pdf or
    .docx, case-insensitive). Relative paths are resolved against the
    server's working directory, so prefer absolute paths. Raises an error if
    the file does not exist or has an unsupported extension.

    When to use:
    - When you need the text of a Word or PDF document stored on the server's disk
    - When you know the file's path but don't have its contents

    When not to use:
    - When you already have the file's contents; use binary_document_to_markdown
    - For files that are already plain text or markdown; read them directly
    - For formats other than DOCX and PDF (including legacy .doc)

    Examples:
    >>> document_path_to_markdown("C:/Users/me/Documents/report.docx")
    '# Report Title\\n\\nFirst paragraph of the report...'
    >>> document_path_to_markdown("/home/me/papers/paper.PDF")
    'Paper Title\\n\\nAbstract text...'
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"No file found at {file_path}")

    file_type = SUPPORTED_EXTENSIONS.get(path.suffix.lower())
    if file_type is None:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'; expected .pdf or .docx"
        )

    return _bytes_to_markdown(path.read_bytes(), file_type)
