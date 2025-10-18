# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI-Powered Web Scraper** - A Python-based command-line tool that fetches web pages, extracts content using BeautifulSoup, and generates AI-powered summaries using the Google Gemini API. The tool is designed to be modular and callable by other projects (e.g., Virtual Personal Assistants).

### Core Workflow
1. User provides a URL
2. Tool fetches page content and extracts text
3. Google Gemini API generates a bulleted summary
4. Top 10 unique links are extracted and displayed
5. Interactive CLI allows navigating found links or entering new URLs

## Tech Stack

- **Language:** Python 3
- **HTTP Client:** `requests` - for fetching web pages
- **HTML Parsing:** `BeautifulSoup4` - for extracting text and links
- **AI Summarization:** `google-generativeai` - Gemini API integration
- **URL Handling:** `urllib.parse` - for converting relative to absolute URLs

## Architecture & Key Components

### Main Functions (main.py)

1. **`summarize_text(text)`** (lines 8-25)
   - Configures Gemini API with `GOOGLE_API_KEY` environment variable
   - Uses `gemini-2.5-pro` model
   - Returns bulleted summary or None on error

2. **`fetch_parse_summarize(url)`** (lines 27-70)
   - Fetches URL using requests
   - Parses HTML with BeautifulSoup
   - Extracts and normalizes text
   - Calls `summarize_text()` for AI summary
   - Extracts top 10 unique absolute links using `urljoin()`
   - Implements error handling for network and parsing failures

3. **Interactive CLI Loop** (lines 72-98)
   - Main entry point prompting for starting URL
   - Displays summary and link options
   - Accepts: link numbers (1-10), 'new' (enter new URL), or 'exit'

### Error Handling Pattern

- Try-catch blocks in both main functions
- Environment variable validation for API key
- HTTP error handling with `raise_for_status()`
- User input validation in CLI loop

## Setup & Running

### Initial Setup
```bash
# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests beautifulsoup4 google-generativeai

# Set API key (required)
export GOOGLE_API_KEY="YOUR_API_KEY"
```

### Running the Application
```bash
python main.py
```

### Interactive Usage
- Enter URL when prompted
- Review AI summary and available links
- Choose: link number (1-10), 'new' for new URL, or 'exit' to quit

## Development Notes

### Dependency Management
- All Python dependencies managed via `venv` directory (excluded from git)
- No `requirements.txt` currently - dependencies installed manually
- `package.json` includes `node-pty` (likely for future terminal integration)

### Security & API Keys
- API keys handled exclusively via environment variables
- Never hardcoded in source code

### Modularity Design
- Code organized into focused functions with single responsibilities
- Easy for other projects to import and use `fetch_parse_summarize()` function
- Clean separation between scraping logic, AI interaction, and CLI

## Future Expansion Areas

- Add `requirements.txt` for easier dependency management
- Implement unit tests (currently no test framework)
- Add CI/CD configuration (GitHub Actions)
- Consider Docker containerization for deployment
- Type hints for better code clarity
- Configurable models and parameters (currently hardcoded to gemini-2.5-pro)
