import os
import sys
import json
import asyncio
from pathlib import Path
import google.generativeai as genai
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.async_api import async_playwright, Page

def load_config():
    """
    Loads configuration from a JSON file.
    - Prioritizes path from command-line argument.
    - Falls back to checking the current directory.
    - Finally, checks the script's directory.
    - Returns a default if no file is found or is invalid.
    """
    config_path = None
    # 1. Check for command-line argument
    if len(sys.argv) > 1:
        path_from_arg = Path(sys.argv[1])
        if path_from_arg.is_file():
            config_path = path_from_arg
        else:
            print(f"Warning: Config file not found at command-line path: {path_from_arg}")

    # 2. Check current working directory (if no valid CLI path)
    if not config_path:
        path_in_cwd = Path('config.json')
        if path_in_cwd.is_file():
            config_path = path_in_cwd

    # 3. Check script's directory (if still not found)
    if not config_path:
        script_dir_path = Path(__file__).parent / 'config.json'
        if script_dir_path.is_file():
            config_path = script_dir_path

    # Load the config if a path was found
    if config_path:
        print(f"Loading configuration from: {config_path}")
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load or parse config file. Using defaults. Error: {e}")
    
    print("Using default configuration.")
    return {"model_name": "gemini-pro"} # Default config

def summarize_text(text, model_name):
    """
    Uses the Gemini API to summarize the given text into a bulleted list.
    """
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            return None
        genai.configure(api_key=api_key)

        print(f"Using generative model: {model_name}")
        model = genai.GenerativeModel(model_name)
        prompt = f"Summarize the following text from a website into a concise, bulleted list of the main points:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None

async def fetch_parse_summarize(page: Page, url: str, model_name: str):
    """
    Fetches, parses, and summarizes a URL using an existing Playwright Page.
    Returns a list of the top 10 unique, absolute links found.
    """
    try:
        print(f"\nFetching content from {url}...")
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        content = await page.content()

        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        if not text:
            print("Could not extract any text from the page.")
            return []

        print("Summarizing content...")
        summary = summarize_text(text, model_name)
        if summary:
            print("\n--- AI Summary ---")
            print(summary)
            print("------------------\n")

        raw_links = [a['href'] for a in soup.find_all('a', href=True)]
        unique_links = list(dict.fromkeys([urljoin(url, link) for link in raw_links]))
        
        top_links = unique_links[:10]

        if top_links:
            print("--- Found Links ---")
            for i, link in enumerate(top_links):
                print(f"[{i + 1}] {link}")
            print("-------------------")
        
        return top_links

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

async def main(model_name: str):
    """
    Main function to run the interactive scraping loop.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        current_url = input("Please enter the URL to start scraping: ")
        
        if current_url:
            print("Navigating to the initial URL...")
            await page.goto(current_url, wait_until='domcontentloaded', timeout=60000)

        while current_url:
            login_attempt = input("Does this page require a login? (y/n): ").lower()
            if login_attempt == 'y':
                print("\n>>> Please perform the login in the browser window. <<<")
                input(">>> Press Enter here after you have successfully logged in... <<<")
                print("Resuming scraping...")

            links_found = await fetch_parse_summarize(page, page.url, model_name)

            if not links_found:
                print("\nNo links to follow from this page.")
            
            prompt = "\nEnter a number to follow a link, 'new' to enter a new URL, or 'exit' to quit: "
            user_choice = input(prompt).lower()

            if user_choice == 'exit':
                break
            elif user_choice == 'new':
                current_url = input("Please enter the new URL: ")
                if current_url:
                    await page.goto(current_url, wait_until='domcontentloaded', timeout=60000)
            else:
                try:
                    choice_index = int(user_choice) - 1
                    if 0 <= choice_index < len(links_found):
                        current_url = links_found[choice_index]
                    else:
                        print("Invalid number. Please try again.")
                        current_url = page.url
                except ValueError:
                    print("Invalid input. Please enter a number, 'new', or 'exit'.")
                    current_url = page.url
        
        await browser.close()
    
    print("\nScraping session finished. Goodbye!")

if __name__ == "__main__":
    config = load_config()
    model = config.get("model_name", "gemini-pro") # Final fallback
    asyncio.run(main(model_name=model))