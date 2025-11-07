#!/usr/bin/env python3
"""
Targeted SSA Blue Book Adult Listings Crawler

This script specifically crawls all adult impairment listings from the SSA Blue Book.
It extracts the links from the existing scraped data and fetches the actual listing pages.

Usage:
    python crawl_adult_listings.py [--provider provider_name]
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

from crawler import WebsiteCrawler
from ai_converter import AIDataConverter


# Complete list of SSA Adult Listings URLs
ADULT_LISTING_URLS = [
    "https://www.ssa.gov/disability/professionals/bluebook/1.00-Musculoskeletal-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/2.00-SpecialSensesandSpeech-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/3.00-Respiratory-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/4.00-Cardiovascular-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/5.00-Digestive-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/6.00-Genitourinary-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/7.00-HematologicalDisorders-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/8.00-Skin-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/9.00-Endocrine-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/10.00-MultipleBody-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/11.00-Neurological-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/12.00-MentalDisorders-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/13.00-Cancer-Adult.htm",
    "https://www.ssa.gov/disability/professionals/bluebook/14.00-Immune-Adult.htm",
]


async def crawl_adult_listings(output_dir="./ssa_adult_listings"):
    """Crawl all adult listing pages."""
    print("="*70)
    print("SSA BLUE BOOK - ADULT LISTINGS TARGETED CRAWLER")
    print("="*70)
    print()
    print(f"Will crawl {len(ADULT_LISTING_URLS)} adult listing pages")
    print(f"Output directory: {output_dir}")
    print()

    # Use the existing crawler but with specific URL list
    # We'll crawl each page individually at depth 0 to get just those pages
    from playwright.async_api import async_playwright
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    import hashlib
    import time

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    html_dir = output_path / "html"
    html_dir.mkdir(exist_ok=True)
    json_dir = output_path / "json"
    json_dir.mkdir(exist_ok=True)

    scraped_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        for i, url in enumerate(ADULT_LISTING_URLS, 1):
            print(f"[{i}/{len(ADULT_LISTING_URLS)}] Fetching: {url}")

            try:
                response = await page.goto(url, wait_until='domcontentloaded', timeout=60000)

                if not response or response.status >= 400:
                    print(f"  ⚠️  Failed: HTTP {response.status if response else 'No response'}")
                    continue

                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')

                # Extract data
                text = soup.get_text(separator=' ', strip=True)
                title = soup.find('title')
                title_text = title.get_text(strip=True) if title else ''

                # Extract headings
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

                # Save HTML
                url_hash = hashlib.md5(url.encode()).hexdigest()
                html_file = html_dir / f"{url_hash}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                page_data = {
                    'url': url,
                    'url_hash': url_hash,
                    'title': title_text,
                    'text_content': text,
                    'headings': headings,
                    'tables': tables,
                    'links': [],  # Not extracting links for targeted crawl
                    'html_file': str(html_file),
                    'fetched_at': time.time()
                }

                scraped_data.append(page_data)
                print(f"  ✓ Success: {title_text[:60]}...")
                print(f"    Headings: {len(headings)}, Tables: {len(tables)}")

                # Polite delay
                await asyncio.sleep(2.0)

            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue

        await browser.close()

    # Save data
    output_file = json_dir / "scraped_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

    print()
    print("="*70)
    print("CRAWLING COMPLETE")
    print("="*70)
    print(f"Pages successfully crawled: {len(scraped_data)}/{len(ADULT_LISTING_URLS)}")
    print(f"Data saved to: {output_file}")
    print()

    return scraped_data, output_file


def convert_to_json(scraped_data, output_file, provider="gemini"):
    """Convert scraped data to structured JSON."""
    print("="*70)
    print("CONVERTING TO STRUCTURED JSON")
    print("="*70)
    print()

    try:
        converter = AIDataConverter(provider=provider)
    except Exception as e:
        print(f"ERROR: Could not initialize {provider} provider: {e}")
        print("\nMake sure you have set the appropriate API key:")
        print("  - Gemini: export GOOGLE_API_KEY=your-key")
        print("  - Claude: export ANTHROPIC_API_KEY=your-key")
        print("  - OpenAI: export OPENAI_API_KEY=your-key")
        print("  - Grok: export XAI_API_KEY=your-key")
        return None

    # Analyze and generate schema
    print("Analyzing Blue Book structure...")
    analysis = converter.analyze_data_structure(scraped_data)

    print(f"\nAnalysis Results:")
    print(f"  Content Type: {analysis.get('content_type', 'Unknown')}")
    print(f"  Entities: {', '.join(analysis.get('entities', []))}")

    # Save schema
    output_path = Path(output_file).parent.parent
    schema_file = output_path / "json" / "schema_analysis.json"
    with open(schema_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"  Schema saved: {schema_file}")

    # Convert data
    final_output = output_path / f"ssa_bluebook_adult_complete.json"
    schema = analysis.get('schema', {})

    if schema:
        print(f"\nConverting {len(scraped_data)} pages...")
        structured_data = converter.convert_all_pages(
            scraped_data,
            schema,
            str(final_output),
            batch_size=5,
            delay=2.0
        )
        return final_output
    else:
        print("ERROR: No schema generated")
        return None


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Crawl SSA Adult Listings")
    parser.add_argument("--provider", choices=["gemini", "claude", "openai", "grok"],
                       default="gemini", help="AI provider for conversion")
    parser.add_argument("--crawl-only", action="store_true",
                       help="Only crawl, skip AI conversion")
    parser.add_argument("--output-dir", default="./ssa_adult_listings",
                       help="Output directory")

    args = parser.parse_args()

    # Crawl
    scraped_data, data_file = await crawl_adult_listings(args.output_dir)

    if not scraped_data:
        print("\nNo data was scraped. Exiting.")
        sys.exit(1)

    # Convert (unless skipped)
    if not args.crawl_only:
        final_file = convert_to_json(scraped_data, data_file, args.provider)

        if final_file:
            print()
            print("="*70)
            print("SUCCESS!")
            print("="*70)
            print(f"\nComplete SSA Adult Blue Book data:")
            print(f"  📄 Structured JSON: {final_file}")
            print(f"  📋 Schema: {Path(data_file).parent / 'schema_analysis.json'}")
            print(f"  📁 Raw data: {data_file}")
            print()
            print("Your data is ready for database import!")
    else:
        print("\nCrawling complete. Run conversion separately with:")
        print(f"  python salvage_scraped_data.py {data_file} --provider {args.provider}")


if __name__ == "__main__":
    asyncio.run(main())
