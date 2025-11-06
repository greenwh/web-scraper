"""
Website Data Retrieval Module
Provides recursive crawling capabilities similar to wget -m or HTTrack
"""

import os
import asyncio
import json
import hashlib
from pathlib import Path
from typing import Set, Dict, List, Optional
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
import time


class WebsiteCrawler:
    """
    Recursive website crawler that downloads and stores website content offline.
    """

    def __init__(
        self,
        base_url: str,
        output_dir: str = "./scraped_data",
        max_depth: int = 3,
        same_domain_only: bool = True,
        delay: float = 1.0,
        max_pages: int = 100,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ):
        """
        Initialize the crawler.

        Args:
            base_url: Starting URL for crawling
            output_dir: Directory to store scraped data
            max_depth: Maximum depth for recursive crawling
            same_domain_only: Only crawl URLs from the same domain
            delay: Delay between requests in seconds
            max_pages: Maximum number of pages to crawl
            include_patterns: List of URL patterns to include (substring match)
            exclude_patterns: List of URL patterns to exclude (substring match)
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.max_depth = max_depth
        self.same_domain_only = same_domain_only
        self.delay = delay
        self.max_pages = max_pages
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []

        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict] = []
        self.base_domain = urlparse(base_url).netloc

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.html_dir = self.output_dir / "html"
        self.html_dir.mkdir(exist_ok=True)
        self.json_dir = self.output_dir / "json"
        self.json_dir.mkdir(exist_ok=True)

    def _should_crawl(self, url: str) -> bool:
        """Check if a URL should be crawled based on filters."""
        # Check if already visited
        if url in self.visited_urls:
            return False

        # Check max pages limit
        if len(self.visited_urls) >= self.max_pages:
            return False

        parsed = urlparse(url)

        # Check domain restriction
        if self.same_domain_only and parsed.netloc != self.base_domain:
            return False

        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if pattern in url:
                return False

        # Check include patterns (if specified, URL must match at least one)
        if self.include_patterns:
            if not any(pattern in url for pattern in self.include_patterns):
                return False

        # Skip common non-content URLs
        skip_extensions = ['.pdf', '.jpg', '.png', '.gif', '.css', '.js', '.zip', '.exe']
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False

        return True

    def _get_url_hash(self, url: str) -> str:
        """Generate a hash for URL to use as filename."""
        return hashlib.md5(url.encode()).hexdigest()

    async def _fetch_page(self, page: Page, url: str) -> Optional[Dict]:
        """Fetch and parse a single page."""
        try:
            print(f"Fetching: {url}")

            # Navigate to the page
            response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)

            if not response or response.status >= 400:
                print(f"Failed to fetch {url}: HTTP {response.status if response else 'No response'}")
                return None

            # Get page content
            content = await page.content()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Extract text content
            text = soup.get_text(separator=' ', strip=True)

            # Extract all links
            raw_links = [a.get('href') for a in soup.find_all('a', href=True)]
            absolute_links = [urljoin(url, link) for link in raw_links if link]

            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else ''

            # Get headings for structure
            headings = []
            for level in range(1, 7):
                for heading in soup.find_all(f'h{level}'):
                    headings.append({
                        'level': level,
                        'text': heading.get_text(strip=True)
                    })

            # Extract tables
            tables = []
            for table in soup.find_all('table'):
                table_data = []
                rows = table.find_all('tr')
                for row in rows:
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    if cells:
                        table_data.append(cells)
                if table_data:
                    tables.append(table_data)

            # Save HTML to file
            url_hash = self._get_url_hash(url)
            html_file = self.html_dir / f"{url_hash}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

            page_data = {
                'url': url,
                'url_hash': url_hash,
                'title': title_text,
                'text_content': text,
                'headings': headings,
                'tables': tables,
                'links': absolute_links,
                'html_file': str(html_file),
                'fetched_at': time.time()
            }

            return page_data

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def _crawl_recursive(
        self,
        page: Page,
        url: str,
        current_depth: int = 0
    ):
        """Recursively crawl pages starting from the given URL."""
        # Check if we should crawl this URL
        if not self._should_crawl(url):
            return

        # Check depth limit
        if current_depth > self.max_depth:
            return

        # Mark as visited
        self.visited_urls.add(url)

        # Fetch the page
        page_data = await self._fetch_page(page, url)

        if not page_data:
            return

        # Store the data
        self.scraped_data.append(page_data)

        # Save incremental progress
        progress_file = self.json_dir / "crawl_progress.json"
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_pages': len(self.scraped_data),
                'visited_urls': list(self.visited_urls),
                'last_url': url
            }, f, indent=2)

        print(f"Crawled {len(self.scraped_data)}/{self.max_pages} pages (depth: {current_depth})")

        # Extract and follow links
        if current_depth < self.max_depth:
            for link in page_data['links']:
                if self._should_crawl(link):
                    # Add delay to be polite
                    await asyncio.sleep(self.delay)
                    await self._crawl_recursive(page, link, current_depth + 1)

    async def crawl(self) -> List[Dict]:
        """
        Start the crawling process.

        Returns:
            List of scraped page data
        """
        print(f"Starting crawl of {self.base_url}")
        print(f"Max depth: {self.max_depth}, Max pages: {self.max_pages}")
        print(f"Same domain only: {self.same_domain_only}")
        print(f"Output directory: {self.output_dir}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Set a realistic user agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })

            try:
                await self._crawl_recursive(page, self.base_url, 0)
            finally:
                await browser.close()

        # Save final data
        output_file = self.json_dir / "scraped_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)

        print(f"\nCrawling complete!")
        print(f"Total pages crawled: {len(self.scraped_data)}")
        print(f"Data saved to: {output_file}")

        return self.scraped_data


async def main():
    """Example usage of the WebsiteCrawler."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python crawler.py <url> [max_depth] [max_pages]")
        print("Example: python crawler.py https://example.com 2 50")
        return

    url = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    crawler = WebsiteCrawler(
        base_url=url,
        max_depth=max_depth,
        max_pages=max_pages,
        delay=1.0
    )

    await crawler.crawl()


if __name__ == "__main__":
    asyncio.run(main())
