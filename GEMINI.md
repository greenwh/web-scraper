# Project: AI-Powered Web Scraper

## Project Overview

This project is a Python-based, interactive command-line web scraper. It uses **Playwright** to launch a real browser, allowing it to handle modern, JavaScript-heavy websites and pages requiring a login.

The tool takes a starting URL, navigates to the page, and gives the user an opportunity to perform a manual login if needed. Once the user confirms, it scrapes the page content, uses the Google Gemini API to generate a concise, bulleted summary, and extracts the top 10 unique hyperlinks.

The scraper then enters an interactive loop, allowing the user to select a link to follow, enter a new URL, or exit. This creates a powerful way to "crawl" and understand websites through AI-generated summaries, even those behind authentication.

The core technologies used are:
-   **Python 3:** The main programming language.
-   **Playwright:** For browser automation and fetching dynamic web page content.
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
All required libraries are listed in `requirements.txt`. Install them using pip:
```bash
pip install -r requirements.txt
```

**Install browser binaries:**
Playwright requires browser binaries to function. Install them with this command:
```bash
playwright install
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
The script will open a browser window and prompt you to enter a URL. If the site requires a login, you can perform it in the browser window.

You can also specify a path to a custom configuration file:
```bash
python main.py /path/to/your/config.json
```

## Development Conventions

-   **Dependency Management:** All dependencies are managed with `pip` and a `requirements.txt` file within a Python virtual environment (`venv`).
-   **Configuration:** The Gemini model is configured via a `config.json` file. The script searches for this file in the command-line path, the current directory, and the script's directory before using a default.
-   **API Keys:** API keys are handled securely via environment variables and are not hardcoded.
-   **Modularity:** The code is organized into functions with specific responsibilities, such as `summarize_text`, `fetch_parse_summarize`, and `load_config`.