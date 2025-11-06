# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI-Powered Web Scraper** - A Python-based command-line tool with two operational modes:

### Mode 1: Interactive Browsing (`main.py`)
- Browse websites interactively with AI-powered summaries
- Navigate through links or enter new URLs
- Real-time content analysis and summarization

### Mode 2: Data Retrieval & JSON Export (`scrape_to_json.py`) - **NEW**
- Recursive website crawling (similar to `wget -m` or HTTrack)
- Offline data storage for later use
- AI-powered conversion to structured JSON for database integration
- Multi-AI provider support (Gemini, Claude, OpenAI)
- Automatic schema generation and documentation

### Core Workflows

**Interactive Mode:**
1. User provides a URL
2. Tool fetches page content and extracts text
3. AI generates a bulleted summary
4. Top 10 unique links are extracted and displayed
5. User navigates or enters new URLs

**Data Retrieval Mode:**
1. Recursively crawl website with configurable depth/limits
2. Extract and store content offline (HTML + structured data)
3. AI analyzes content structure and generates optimal JSON schema
4. Convert all pages to structured JSON following the schema
5. Generate documentation for database integration

## Tech Stack

- **Language:** Python 3
- **Browser Automation:** `playwright` - for JavaScript-enabled scraping and interactive browsing
- **HTML Parsing:** `BeautifulSoup4` - for extracting text, links, and tables
- **AI Providers:**
  - `google-generativeai` - Gemini API (default, cost-effective)
  - `anthropic` - Claude API (high accuracy for complex structures)
  - `openai` - GPT API (balanced performance)
- **URL Handling:** `urllib.parse` - for converting relative to absolute URLs
- **Data Storage:** JSON files with metadata and schema documentation

## Architecture & Key Components

### Interactive Mode (main.py)

1. **`summarize_text(text, model_name)`**
   - Configures Gemini API with `GOOGLE_API_KEY` environment variable
   - Supports configurable models via config.json
   - Returns bulleted summary or None on error

2. **`fetch_parse_summarize(page, url, model_name)`**
   - Uses Playwright Page object for rendering JavaScript
   - Parses HTML with BeautifulSoup
   - Extracts and normalizes text
   - Calls `summarize_text()` for AI summary
   - Extracts top 10 unique absolute links using `urljoin()`
   - Implements error handling for network and parsing failures

3. **`main(model_name)`**
   - Async function managing browser session
   - Interactive CLI loop for navigation
   - Login support for authenticated pages
   - Accepts: link numbers (1-10), 'new' (enter new URL), or 'exit'

### Data Retrieval Mode (New Modules)

#### crawler.py - Website Crawling Engine

**Class: `WebsiteCrawler`**
- Recursive crawling with depth and page limits
- Domain filtering and URL pattern matching
- Polite crawling with configurable delays
- Offline storage of HTML and structured data
- Progress tracking and resumption support

**Key Methods:**
- `__init__()` - Configure crawler parameters
- `crawl()` - Main entry point, returns list of scraped data
- `_crawl_recursive()` - Recursive crawling logic
- `_fetch_page()` - Fetch and parse single page
- `_should_crawl()` - URL filtering logic

**Output:**
- `html/*.html` - Raw HTML files
- `json/scraped_data.json` - Structured page data
- `json/crawl_progress.json` - Progress tracking

#### ai_converter.py - AI-Powered JSON Conversion

**Classes:**
- `AIProvider` (ABC) - Base class for AI providers
- `GeminiProvider` - Google Gemini implementation
- `ClaudeProvider` - Anthropic Claude implementation
- `OpenAIProvider` - OpenAI GPT implementation
- `AIDataConverter` - Main conversion coordinator

**Key Methods:**
- `analyze_data_structure()` - AI analyzes content and generates schema
- `convert_page_to_structured_data()` - Convert single page using schema
- `convert_all_pages()` - Batch conversion with progress saves

**Output:**
- `schema_analysis.json` - AI-generated schema and metadata
- `structured_data_*.json` - Final structured JSON for database

#### scrape_to_json.py - Main Integration Script

**Functions:**
- `parse_arguments()` - Command-line argument parsing
- `crawl_website()` - Execute crawling phase
- `convert_to_json()` - Execute AI conversion phase
- `generate_documentation()` - Create README with database examples
- `main()` - Orchestrate complete pipeline

**Features:**
- Comprehensive CLI with help text
- Progress reporting at each phase
- Error handling and recovery
- Automatic documentation generation

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

# Install all dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Set API key(s) - at least one required for data retrieval mode
export GOOGLE_API_KEY="YOUR_API_KEY"        # For Gemini (default)
export ANTHROPIC_API_KEY="YOUR_API_KEY"     # For Claude (optional)
export OPENAI_API_KEY="YOUR_API_KEY"        # For OpenAI (optional)
```

### Running Interactive Mode
```bash
python main.py [config.json]

# Interactive usage:
# - Enter URL when prompted
# - Review AI summary and available links
# - Choose: link number (1-10), 'new' for new URL, or 'exit' to quit
# - Can log in to authenticated sites when prompted
```

### Running Data Retrieval Mode

**Basic usage:**
```bash
python scrape_to_json.py <url>
```

**SSA Blue Book example (primary use case):**
```bash
# See examples/ssa_bluebook_config.sh for full configuration
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --provider gemini \
    --output ssa_bluebook.json
```

**Advanced options:**
```bash
python scrape_to_json.py https://example.com \
    --max-depth 2 \
    --max-pages 50 \
    --delay 2.0 \
    --provider claude \
    --include "/docs/" \
    --exclude "/archive/" \
    --output mydata.json \
    --output-dir ./my_scraped_data
```

**For detailed usage:** See `DATA_RETRIEVAL_README.md`

## Development Notes

### Project Structure
```
web-scraper/
├── main.py                      # Interactive browsing mode
├── scrape_to_json.py           # Data retrieval & JSON export
├── crawler.py                   # Website crawling engine
├── ai_converter.py              # AI-powered JSON conversion
├── requirements.txt             # Python dependencies
├── test_modules.py              # Module tests
├── CLAUDE.md                    # This file
├── DATA_RETRIEVAL_README.md    # Detailed data retrieval docs
├── examples/
│   └── ssa_bluebook_config.sh  # SSA Blue Book example
└── scraped_data/                # Output directory (created on first run)
    ├── html/                    # Raw HTML files
    ├── json/                    # Raw + structured JSON
    └── README.md                # Auto-generated documentation
```

### Dependency Management
- All Python dependencies in `requirements.txt`
- Managed via `venv` (excluded from git)
- Key dependencies:
  - `playwright` - Browser automation
  - `beautifulsoup4` - HTML parsing
  - `google-generativeai` - Gemini AI
  - `anthropic` - Claude AI (optional)
  - `openai` - GPT AI (optional)

### Security & API Keys
- API keys handled exclusively via environment variables
- Never hardcoded in source code
- Multiple provider support allows choosing based on security preferences
- Rate limiting and delays prevent abuse

### Modularity Design
- Clean separation between modules:
  - `crawler.py` - Independent crawling (no AI dependency)
  - `ai_converter.py` - Independent conversion (works with any data)
  - `scrape_to_json.py` - Orchestration layer
- Easy to import and use in other projects
- Provider pattern for AI services enables easy extension
- ABC base class makes adding new providers straightforward

### Testing
- `test_modules.py` - Unit tests for core functionality
- Tests crawling, filtering, data structures
- Mock-friendly design for testing without API calls
- Run with: `python test_modules.py`

## Use Cases

### Primary: SSA Blue Book Retrieval
Extract complete Social Security disability criteria for offline database use.

### Secondary Use Cases:
1. **Medical/Legal Documentation** - Archive structured professional content
2. **Technical Documentation** - Create offline documentation databases
3. **Product Catalogs** - Extract e-commerce product data
4. **Knowledge Bases** - Convert web knowledge bases to searchable JSON
5. **Research Archives** - Structured archival of research websites

## Key Features Implemented

✅ Recursive website crawling with depth/page limits
✅ JavaScript-enabled scraping via Playwright
✅ Offline HTML and data storage
✅ Multi-AI provider support (Gemini, Claude, OpenAI)
✅ Automatic schema generation from content analysis
✅ Structured JSON export with metadata
✅ Database integration documentation
✅ Progress tracking and resumption
✅ Configurable filtering and rate limiting
✅ Comprehensive error handling
✅ Automatic documentation generation
✅ Support for textual and tabular data

## Future Expansion Areas

- ✅ `requirements.txt` added
- Docker containerization for easier deployment
- Resume capability for interrupted AI conversions
- Parallel processing for faster conversions
- Specialized extractors for common site types (WordPress, etc.)
- Web UI for configuration and monitoring
- Incremental updates (re-crawl changed pages only)
- Export to additional formats (CSV, XML, SQLite directly)
- Custom schema templates for common use cases
