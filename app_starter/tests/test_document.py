import asyncio
import base64
import binascii
import os
import shutil
import pytest
from main import mcp
from tools.document import binary_document_to_markdown, document_path_to_markdown


def read_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read base64-encoded content from the fixture
        docx_data = read_base64(self.DOCX_FIXTURE)

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read base64-encoded content from the fixture
        pdf_data = read_base64(self.PDF_FIXTURE)

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_rejects_invalid_base64(self):
        """Test that data which is not base64 raises an error."""
        with pytest.raises(binascii.Error):
            binary_document_to_markdown("not base64!", "pdf")

    def test_binary_document_to_markdown_through_mcp_server(self):
        """Test calling the tool through the MCP server with JSON arguments."""
        pdf_data = read_base64(self.PDF_FIXTURE)
        direct = binary_document_to_markdown(pdf_data, "pdf")

        content = asyncio.run(
            mcp.call_tool(
                "binary_document_to_markdown",
                {"binary_data": pdf_data, "file_type": "pdf"},
            )
        )

        assert content[0].text == direct


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = TestBinaryDocumentToMarkdown.FIXTURES_DIR
    DOCX_FIXTURE = TestBinaryDocumentToMarkdown.DOCX_FIXTURE
    PDF_FIXTURE = TestBinaryDocumentToMarkdown.PDF_FIXTURE

    def test_document_path_to_markdown_with_docx(self):
        """Test converting a DOCX file by path matches the base64 tool."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        assert len(result) > 0
        assert result == binary_document_to_markdown(
            read_base64(self.DOCX_FIXTURE), "docx"
        )

    def test_document_path_to_markdown_with_pdf(self):
        """Test converting a PDF file by path matches the base64 tool."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        assert len(result) > 0
        assert result == binary_document_to_markdown(
            read_base64(self.PDF_FIXTURE), "pdf"
        )

    def test_document_path_to_markdown_uppercase_extension(self, tmp_path):
        """Test that the extension is matched case-insensitively."""
        upper = tmp_path / "MCP_DOCS.PDF"
        shutil.copy(self.PDF_FIXTURE, upper)

        assert document_path_to_markdown(str(upper)) == document_path_to_markdown(
            self.PDF_FIXTURE
        )

    def test_document_path_to_markdown_missing_file(self, tmp_path):
        """Test that a path with no file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(tmp_path / "missing.pdf"))

    def test_document_path_to_markdown_unsupported_extension(self, tmp_path):
        """Test that a non-PDF/DOCX file raises ValueError."""
        text_file = tmp_path / "notes.txt"
        text_file.write_text("hello")

        with pytest.raises(ValueError):
            document_path_to_markdown(str(text_file))

    def test_document_path_to_markdown_contains_known_content(self):
        """Test that the fixtures' known text appears in the output."""
        for fixture in (self.DOCX_FIXTURE, self.PDF_FIXTURE):
            result = document_path_to_markdown(fixture)

            assert "Overview" in result
            assert "Key Features of this Python SDK" in result
            assert "Build MCP clients that can connect to any MCP server" in result

    def test_document_path_to_markdown_keeps_docx_structure(self):
        """Test that DOCX headings, lists and tables become markdown."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        lines = result.splitlines()

        assert "# Overview" in lines
        assert "## Key Features of this Python SDK" in lines
        assert "* Build MCP clients that can connect to any MCP server" in lines
        assert "| --- | --- | --- | --- |" in lines

    def test_document_path_to_markdown_directory(self, tmp_path):
        """Test that a directory path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(str(tmp_path))

    def test_document_path_to_markdown_relative_path(self, monkeypatch):
        """Test that a relative path resolves against the working directory."""
        monkeypatch.chdir(self.FIXTURES_DIR)

        assert document_path_to_markdown("mcp_docs.pdf") == document_path_to_markdown(
            self.PDF_FIXTURE
        )

    def test_document_path_to_markdown_path_with_spaces_and_unicode(self, tmp_path):
        """Test a path containing spaces and non-ASCII characters."""
        folder = tmp_path / "mis docs"
        folder.mkdir()
        target = folder / "año ñ.docx"
        shutil.copy(self.DOCX_FIXTURE, target)

        assert document_path_to_markdown(str(target)) == document_path_to_markdown(
            self.DOCX_FIXTURE
        )

    def test_document_path_to_markdown_through_mcp_server(self):
        """Test calling the tool through the MCP server with a JSON path."""
        content = asyncio.run(
            mcp.call_tool(
                "document_path_to_markdown", {"file_path": self.DOCX_FIXTURE}
            )
        )

        assert content[0].text == document_path_to_markdown(self.DOCX_FIXTURE)
