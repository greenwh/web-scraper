# Project: AI-Powered Web Scraper

## Project Overview

This project is a Python-based, interactive command-line web scraper. It takes a starting URL from the user, fetches the content, and uses the Google Gemini API to generate a concise, bulleted summary of the page. It also extracts and displays the top 10 unique hyperlinks from the page.

The tool then enters an interactive loop, allowing the user to select one of the found links to scrape next, enter a new URL, or exit the program. This creates a powerful way to "crawl" and understand websites through AI-generated summaries.

The core technologies used are:
-   **Python 3:** The main programming language.
-   **Requests:** For making HTTP requests to fetch web page content.
-   **BeautifulSoup4:** For parsing HTML and extracting text and links.
-   **Google Generative AI (Gemini):** For summarizing the extracted text.

## Building and Running

The project uses a Python virtual environment to manage dependencies.

### 1. Setup and Installation

**Create and activate the virtual environment:**
If the `venv` directory does not exist, create it:
```bash
python3 -m venv venv
```
Activate the environment before running the script:
```bash
source venv/bin/activate
```

**Install dependencies:**
The required libraries are `requests`, `beautifulsoup4`, and `google-generativeai`. Install them using pip:
```bash
pip install requests beautifulsoup4 google-generativeai
```

### 2. Set API Key

The script requires a Google Gemini API key. This must be set as an environment variable named `GOOGLE_API_KEY`.
```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
```

### 3. Running the Script

Once the environment is activated and the API key is set, run the main script:
```bash
python main.py
```
The script will prompt you to enter a URL to begin scraping.

## Development Conventions

-   **Dependency Management:** All dependencies are managed within a Python virtual environment (`venv`). The `.gitignore` file is configured to exclude this directory from version control.
-   **API Keys:** API keys are handled securely via environment variables and are not hardcoded in the source code.
-   **Modularity:** The code is organized into functions with specific responsibilities: `summarize_text` for AI interaction and `fetch_parse_summarize` for the core scraping logic.
