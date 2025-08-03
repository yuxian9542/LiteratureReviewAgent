# Literature Review Agent 📚🤖

An AI-powered academic paper analysis and summarization tool that extracts key insights from PDF research papers using advanced natural language processing.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-green.svg)](https://openai.com/)
[![CLI](https://img.shields.io/badge/interface-CLI-orange.svg)](https://click.palletsprojects.com/)

## ✨ Features

- **📄 PDF Processing**: Extract text from local files or URLs
- **🧠 AI Analysis**: Comprehensive paper analysis using OpenAI GPT models
- **📊 Structured Output**: Results in text, markdown, or JSON formats
- **🔧 Prompt Experimentation**: Multiple prompt versions and custom configurations
- **🌐 URL Support**: Process papers directly from web URLs
- **⚡ Fast & Reliable**: Efficient text processing with progress tracking
- **🔍 Development Tools**: Built-in utilities for prompt testing and comparison

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd LiteraturerReviewAgent

# Install dependencies
pip install -r requirements.txt

# Install as global command (optional)
pip install -e .
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Add your OpenAI API key to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Basic Usage

```bash
# Extract text only (no AI analysis)
python main.py -i paper.pdf

# Full AI analysis
python main.py -i paper.pdf --analyze

# Process from URL with markdown output
python main.py -i https://arxiv.org/pdf/2301.00001.pdf --analyze -f markdown -o analysis.md

# Use as global command (if installed with pip)
litreview -i paper.pdf --analyze
```

## 📖 Usage Guide

### Command Line Options

```bash
litreview [OPTIONS]

Options:
  -i, --input TEXT            PDF file path or URL [required]
  -o, --output TEXT           Output file for analysis
  -f, --format TEXT           Output format: text, markdown, json [default: text]
  --analyze                   Perform AI-powered analysis (requires OpenAI API key)
  -v, --verbose              Enable verbose logging
  --prompt-version TEXT       Prompt version: v1_basic, v2_detailed, v3_structured, experimental
  --custom-prompts TEXT       Use custom prompt configuration
  --list-prompts             List available prompt configurations
  --help                     Show help message
```

### Analysis Output

The AI analysis provides:

- **📝 Summary**: Comprehensive 3-4 paragraph overview
- **🔍 Key Findings**: Bullet-pointed discoveries and results
- **🔬 Methodology**: Research methods and experimental design
- **💡 Contributions**: Novel insights and main contributions
- **⚠️ Limitations**: Identified constraints and future work suggestions

### Output Formats

#### Text Format (Default)
```
============================================================
LITERATURE REVIEW ANALYSIS
============================================================
Generated: 2024-01-15 14:30:25

SUMMARY:
--------
This paper introduces a novel approach to...

KEY FINDINGS:
-------------
1. The proposed method achieves 95% accuracy...
2. Computational complexity is reduced by 40%...
```

#### Markdown Format
```markdown
# Literature Review Analysis
*Generated: 2024-01-15 14:30:25*

## Summary
This paper introduces a novel approach to...

## Key Findings
- The proposed method achieves 95% accuracy...
- Computational complexity is reduced by 40%...
```

#### JSON Format
```json
{
  "timestamp": "2024-01-15T14:30:25",
  "summary": "This paper introduces...",
  "key_findings": ["Finding 1", "Finding 2"],
  "methodology": "The researchers used...",
  "contributions": ["Contribution 1", "Contribution 2"],
  "limitations": ["Limitation 1", "Limitation 2"],
  "metadata": {
    "num_pages": 12,
    "metadata": {...}
  }
}
```

## 🔧 Prompt Experimentation

### Built-in Prompt Versions

- **`v1_basic`**: Simple, direct prompts
- **`v2_detailed`**: Comprehensive with specific instructions (default)
- **`v3_structured`**: Structured output with exact formatting
- **`experimental`**: Testing new approaches (chain-of-thought, confidence scoring)

### Using Different Prompt Versions

```bash
# Try different built-in versions
litreview -i paper.pdf --analyze --prompt-version v1_basic
litreview -i paper.pdf --analyze --prompt-version v3_structured

# List all available prompts
litreview --list-prompts
```

### Custom Prompt Configurations

Create custom prompts by editing YAML files in the `prompts/` directory:

```yaml
# prompts/my_custom.yaml
my_custom:
  system: "You are a domain expert in machine learning."
  
  summary: |
    Analyze this ML paper focusing on:
    - Algorithm novelty
    - Performance metrics
    - Practical applications
    
    Text: {text}
```

Use custom prompts:
```bash
litreview -i paper.pdf --analyze --custom-prompts my_custom
```

## 🛠️ Development Tools

### Prompt Testing Utility

```bash
# Compare two prompt versions
python dev_tools/prompt_tester.py compare-prompts paper.pdf \
  --version1 v2_detailed --version2 v3_structured

# Preview exact prompts
python dev_tools/prompt_tester.py show-prompt summary --version v1_basic

# Create new custom configuration
python dev_tools/prompt_tester.py create-custom-config my_experiment

# List all available prompts
python dev_tools/prompt_tester.py list-prompts
```

### Development Workflow

1. **Experiment with built-in versions**:
   ```bash
   litreview -i test.pdf --analyze --prompt-version v1_basic
   litreview -i test.pdf --analyze --prompt-version v2_detailed
   ```

2. **Create custom prompts**:
   ```bash
   python dev_tools/prompt_tester.py create-custom-config experiment1
   # Edit prompts/experiment1.yaml
   litreview -i test.pdf --analyze --custom-prompts experiment1
   ```

3. **Compare results**:
   ```bash
   python dev_tools/prompt_tester.py compare-prompts test.pdf \
     --version1 v2_detailed --custom2 experiment1 --output comparison.json
   ```

## 🏗️ Architecture

```
LiteraturerReviewAgent/
├── agents/              # AI analysis agents
├── config/              # Configuration management
├── input_handlers/      # Input validation and URL processing
├── parsers/             # PDF text extraction
├── prompts/             # Prompt templates and configurations
├── summarizers/         # Output formatting
├── utils/               # Utility functions
├── dev_tools/           # Development and testing utilities
├── bin/                 # Executable scripts
└── tests/               # Test files
```

### Key Components

- **`LiteratureReviewAgent`**: Main AI analysis engine
- **`PromptTemplates`**: Modular prompt management system
- **`InputValidator`**: PDF validation and URL downloading
- **`AnalysisFormatter`**: Multi-format output generation
- **`PDFParser`**: Text extraction from PDF files

## 📋 Requirements

- Python 3.8+
- OpenAI API key (for AI analysis)
- Internet connection (for URL processing)

### Dependencies

- `openai>=1.0.0` - AI analysis
- `pdfplumber>=0.9.0` - PDF text extraction
- `langchain>=0.1.0` - Text processing and chunking
- `click>=8.1.0` - Command line interface
- `pydantic>=2.0.0` - Configuration management
- `requests>=2.31.0` - URL handling
- `PyYAML>=6.0` - Configuration files

## 🔒 Security & Privacy

- API keys are loaded from environment variables
- Temporary files from URLs are automatically cleaned up
- No data is stored or transmitted beyond OpenAI API calls
- Local processing for all non-AI operations

## 🐛 Troubleshooting

### Common Issues

**API Key Error**:
```bash
Error: OpenAI API key not found
```
Solution: Set `OPENAI_API_KEY` in your `.env` file

**PDF Processing Error**:
```bash
Error: File does not exist or is not a PDF
```
Solution: Ensure the file path is correct and the file is a valid PDF

**Quota Exceeded**:
```bash
Error code: 429 - You exceeded your current quota
```
Solution: Check your OpenAI billing/usage or use without `--analyze` flag

**URL Download Error**:
```bash
Error downloading URL: Connection timeout
```
Solution: Check internet connection and URL accessibility

### Debug Mode

Enable verbose logging for detailed information:
```bash
litreview -i paper.pdf --analyze -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Use development tools
python dev_tools/prompt_tester.py --help
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- The open-source community for the excellent Python libraries
- Academic researchers who make their papers freely available

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the [troubleshooting section](#-troubleshooting)
- Review the [CLAUDE.md](CLAUDE.md) file for detailed technical documentation

---

**Happy researching! 📚✨**