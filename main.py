
import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def summarize_text(text):
    """
    Uses the Gemini API to summarize the given text into a bulleted list.
    """
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            return None
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel('gemini-2.5-pro')
        prompt = f"Summarize the following text from a website into a concise, bulleted list of the main points:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None

def fetch_parse_summarize(url):
    """
    Fetches, parses, and summarizes a URL.
    Returns a list of the top 10 unique, absolute links found.
    """
    try:
        print(f"\nFetching content from {url}...")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        if not text:
            print("Could not extract any text from the page.")
            return []

        print("Summarizing content...")
        summary = summarize_text(text)
        if summary:
            print("\n--- AI Summary ---")
            print(summary)
            print("------------------\n")

        raw_links = [a['href'] for a in soup.find_all('a', href=True)]
        # Create absolute URLs and remove duplicates while preserving order
        unique_links = list(dict.fromkeys([urljoin(url, link) for link in raw_links]))
        
        top_links = unique_links[:10]

        if top_links:
            print("--- Found Links ---")
            for i, link in enumerate(top_links):
                print(f"[{i + 1}] {link}")
            print("-------------------")
        
        return top_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    current_url = input("Please enter the URL to start scraping: ")
    while current_url:
        links_found = fetch_parse_summarize(current_url)

        if not links_found:
            print("\nNo links to follow from this page.")
        
        prompt = "\nEnter a number to follow a link, 'new' to enter a new URL, or 'exit' to quit: "
        user_choice = input(prompt).lower()

        if user_choice == 'exit':
            break
        elif user_choice == 'new':
            current_url = input("Please enter the new URL: ")
        else:
            try:
                choice_index = int(user_choice) - 1
                if 0 <= choice_index < len(links_found):
                    current_url = links_found[choice_index]
                else:
                    print("Invalid number. Please try again.")
                    # Loop will repeat with the same link options
            except ValueError:
                print("Invalid input. Please enter a number, 'new', or 'exit'.")
    
    print("\nScraping session finished. Goodbye!")
