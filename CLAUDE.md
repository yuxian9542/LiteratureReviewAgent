# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Literature Review Agent designed for academic paper analysis and summarization. The project is built in Python and provides a CLI tool for processing PDF documents and extracting text content.

## Setup and Dependencies

The project uses pip for dependency management. Install dependencies with:
```bash
pip install -r requirements.txt
```

Key dependencies include:
- pdfplumber for PDF text extraction
- click for CLI interface
- validators for input validation
- openai and langchain for AI capabilities (future implementation)

## Running the Application

The main entry point is `main.py` which provides a CLI interface:

```bash
# Process a local PDF file
python main.py -i path/to/document.pdf

# Process with output file
python main.py -i path/to/document.pdf -o output.txt

# Show help
python main.py --help
```

## Testing

The project has a `tests/` directory but it's currently empty. There are no specific test commands configured yet.

## Architecture

The codebase follows a modular architecture with clear separation of concerns:

### Core Components

- **`main.py`**: CLI entry point using Click framework
- **`input_handlers/`**: Input validation and classification
  - `InputValidator`: Validates file paths and URLs, currently supports PDF files only
- **`parsers/`**: Document parsing functionality
  - `PDFParser`: Extracts text and metadata from PDF files using pdfplumber
- **`agents/`**: AI agent components (placeholder, not yet implemented)
- **`summarizers/`**: Text summarization components (placeholder, not yet implemented)
- **`config/`**: Configuration management (placeholder)
- **`utils/`**: Utility functions (placeholder)

### Current Implementation Status

The project is in early development:
- ✅ PDF text extraction is functional
- ✅ Input validation for files and URLs
- ⚠️ URL processing is not yet implemented
- ⚠️ AI summarization features are placeholders
- ⚠️ Agent-based processing is not implemented

### Data Flow

1. CLI receives input (file path or URL)
2. `InputValidator` validates and classifies the input
3. For local files: `PDFParser` extracts text and metadata
4. Text output is displayed or saved to file
5. URL processing and AI summarization are planned for future implementation

## Development Notes

- The project expects PDF inputs and validates file extensions
- Error handling is basic and uses print statements
- No logging framework is currently configured
- The codebase is prepared for future AI integration with OpenAI and LangChain dependencies