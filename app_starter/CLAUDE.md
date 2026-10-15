# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Python package of document-related tools (format conversion and processing) exposed to AI assistants through an MCP server built on `FastMCP` from `mcp[cli]==1.8.0`. The project uses `uv`, and the venv lives in `.venv`.

## Commands

```bash
uv venv                    # create the venv (once)
uv pip install -e .        # install in development mode
uv run main.py             # start the MCP server (stdio transport; it blocks, waiting for a client)
uv run pytest              # run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf   # run a single test
uv run mcp dev main.py     # open the server in the MCP Inspector (from mcp[cli])
```

There is no lint or type-check setup.

## Architecture

- `main.py` is the server entry point. It creates `mcp = FastMCP("docs")` and registers tools by calling `mcp.tool()(fn)` on plain functions it imports from `tools/`. A function only becomes a tool once it is registered here.
- `tools/` holds plain Python functions with no MCP imports, one module per area (`math.py`, `document.py`). Because they're plain functions, tests import and call them directly, with no server running.
- `tools/document.py`: `binary_document_to_markdown(binary_data, file_type)` wraps `markitdown`. It decodes the **base64** `binary_data` and passes the bytes in through `BytesIO`, with `StreamInfo(extension=file_type)` telling it the format (`"docx"`, `"pdf"`). Tool arguments arrive as JSON, which can't carry raw bytes, so any tool that takes binary content should take it as a base64 `str`, never as `bytes`.
- `document_path_to_markdown(file_path)` reads a `.pdf`/`.docx` file from the server's disk and detects the format from the extension, ignoring case. It can read any such file the server process can access. Both document tools share the private `_bytes_to_markdown` helper for the actual conversion.
- Registered tools: `add`, `binary_document_to_markdown`, `document_path_to_markdown`. `tests/test_document.py` also calls a tool through `mcp.call_tool(...)` to test the full JSON-argument path.
- `tests/fixtures/` contains the sample files the tests use, `mcp_docs.docx` and `mcp_docs.pdf`.

## Conventions

- Always give function arguments appropriate type hints. This is required for MCP tools, because FastMCP generates their input schema from those hints.

## Defining MCP tools

FastMCP builds each tool's schema from the function itself. The function name becomes the tool name, the docstring becomes the tool description, and each parameter's type hint plus its `Field(description=...)` becomes the input schema. The model on the client side reads these when it decides whether and how to call the tool, so treat them as the tool's documentation.

1. Write the function in a module under `tools/`.
2. Describe every parameter with `pydantic.Field`:
   ```python
   from pydantic import Field

   def my_tool(
       param1: str = Field(description="Detailed description of this parameter"),
       param2: int = Field(description="Explain what this parameter does"),
   ) -> ReturnType:
       """Comprehensive docstring here"""
   ```
3. Write a docstring that:
   - begins with a one-line summary
   - explains in detail what the tool does
   - says when to use the tool, and when not to
   - includes usage examples with their expected input and output
4. Register it in `main.py`: `mcp.tool()(my_tool)`.

`tools/math.py::add` is the reference example: typed `Field` parameters, a one-line summary, a detailed paragraph, a "When to use:" list, and doctest-style `Examples:` showing the expected output.
