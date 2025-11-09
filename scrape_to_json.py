#!/usr/bin/env python3
"""
Website Data Retrieval and JSON Export Tool

This script provides a complete pipeline for:
1. Recursively crawling websites (similar to wget -m or HTTrack)
2. Converting scraped data to structured JSON using AI
3. Generating database-ready JSON with schema documentation

Usage:
    python scrape_to_json.py <url> [options]

Example:
    python scrape_to_json.py https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \\
        --max-depth 3 --max-pages 100 --provider gemini --output ssa_bluebook.json
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

from crawler import WebsiteCrawler
from ai_converter import AIDataConverter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Crawl websites and convert to structured JSON using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Crawl SSA Blue Book with default settings
  python scrape_to_json.py https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm

  # Customize crawling parameters
  python scrape_to_json.py https://example.com --max-depth 2 --max-pages 50 --delay 2.0

  # Use Claude AI for conversion
  python scrape_to_json.py https://example.com --provider claude --output mydata.json

  # Include only specific URL patterns
  python scrape_to_json.py https://example.com --include "/docs/" --include "/api/"

  # Reuse existing schema for consistent parsing
  python scrape_to_json.py https://example.com --schema ./scraped_data/json/schema_analysis.json

AI Providers:
  gemini  - Google Gemini (requires GOOGLE_API_KEY)
  claude  - Anthropic Claude (requires ANTHROPIC_API_KEY)
  openai  - OpenAI GPT (requires OPENAI_API_KEY)
  grok    - xAI Grok (requires XAI_API_KEY)

Schema Reuse:
  Use --schema to provide a pre-existing schema from a previous crawl.
  This ensures consistent data structure across multiple runs or site updates.
        """
    )

    parser.add_argument(
        "url",
        help="Starting URL to crawl"
    )

    # Crawling options
    crawl_group = parser.add_argument_group("Crawling Options")
    crawl_group.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="Maximum depth for recursive crawling (default: 3)"
    )
    crawl_group.add_argument(
        "--max-pages",
        type=int,
        default=100,
        help="Maximum number of pages to crawl (default: 100)"
    )
    crawl_group.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    crawl_group.add_argument(
        "--same-domain",
        action="store_true",
        default=True,
        help="Only crawl URLs from the same domain (default: True)"
    )
    crawl_group.add_argument(
        "--include",
        action="append",
        dest="include_patterns",
        help="Include URLs matching this pattern (can be used multiple times)"
    )
    crawl_group.add_argument(
        "--exclude",
        action="append",
        dest="exclude_patterns",
        help="Exclude URLs matching this pattern (can be used multiple times)"
    )

    # AI conversion options
    ai_group = parser.add_argument_group("AI Conversion Options")
    ai_group.add_argument(
        "--provider",
        choices=["gemini", "claude", "openai", "grok"],
        default="gemini",
        help="AI provider for data conversion (default: gemini)"
    )
    ai_group.add_argument(
        "--skip-conversion",
        action="store_true",
        help="Skip AI conversion, only crawl and save raw data"
    )
    ai_group.add_argument(
        "--conversion-delay",
        type=float,
        default=2.0,
        help="Delay between AI API calls in seconds (default: 2.0)"
    )
    ai_group.add_argument(
        "--schema",
        type=str,
        help="Path to existing schema JSON file for consistent parsing (optional)"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output JSON file path (default: auto-generated)"
    )
    output_group.add_argument(
        "--output-dir",
        default="./scraped_data",
        help="Directory for scraped data (default: ./scraped_data)"
    )

    return parser.parse_args()


async def crawl_website(args) -> tuple[Path, list]:
    """
    Crawl the website and save raw data.

    Returns:
        Tuple of (output_dir, scraped_data)
    """
    print("="*70)
    print("STEP 1: CRAWLING WEBSITE")
    print("="*70)

    crawler = WebsiteCrawler(
        base_url=args.url,
        output_dir=args.output_dir,
        max_depth=args.max_depth,
        same_domain_only=args.same_domain,
        delay=args.delay,
        max_pages=args.max_pages,
        include_patterns=args.include_patterns or [],
        exclude_patterns=args.exclude_patterns or []
    )

    scraped_data = await crawler.crawl()

    return Path(args.output_dir), scraped_data


def convert_to_json(args, output_dir: Path, scraped_data: list) -> Path:
    """
    Convert scraped data to structured JSON using AI.

    Returns:
        Path to the output JSON file
    """
    print("\n" + "="*70)
    print("STEP 2: CONVERTING TO STRUCTURED JSON")
    print("="*70)

    # Initialize AI converter
    converter = AIDataConverter(provider=args.provider)

    # Check if a schema file was provided
    if args.schema:
        print(f"\nUsing provided schema from: {args.schema}")
        try:
            with open(args.schema, 'r', encoding='utf-8') as f:
                schema_data = json.load(f)

            # If the file contains a full analysis with 'schema' key, extract it
            if 'schema' in schema_data:
                analysis = schema_data
                print("Loaded schema from analysis file")
            else:
                # Otherwise, assume the file is the schema itself
                analysis = {
                    'content_type': 'Provided schema',
                    'entities': [],
                    'schema': schema_data,
                    'indexes': [],
                    'notes': 'Schema provided by user for consistent parsing'
                }
                print("Loaded schema directly from file")

            print(f"  Content Type: {analysis.get('content_type', 'Unknown')}")
            print(f"  Using pre-defined schema for consistent parsing")

        except FileNotFoundError:
            print(f"ERROR: Schema file not found: {args.schema}")
            print("Falling back to automatic schema generation...")
            analysis = converter.analyze_data_structure(scraped_data)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in schema file: {e}")
            print("Falling back to automatic schema generation...")
            analysis = converter.analyze_data_structure(scraped_data)
    else:
        # Analyze data structure automatically
        print("\nAnalyzing data structure...")
        analysis = converter.analyze_data_structure(scraped_data)

        print(f"\nData Analysis:")
        print(f"  Content Type: {analysis.get('content_type', 'Unknown')}")
        print(f"  Entities: {', '.join(analysis.get('entities', []))}")

    # Save analysis
    analysis_file = output_dir / "json" / "schema_analysis.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"  Schema saved to: {analysis_file}")

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"structured_data_{timestamp}.json"

    # Convert all pages
    print(f"\nConverting {len(scraped_data)} pages to structured JSON...")
    schema = analysis.get('schema', {})

    if not schema:
        print("WARNING: No schema was generated. Saving raw data instead.")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    else:
        structured_data = converter.convert_all_pages(
            scraped_data,
            schema,
            str(output_file),
            batch_size=5,
            delay=args.conversion_delay
        )

    return output_file


def generate_documentation(output_dir: Path, output_file: Path, args):
    """Generate documentation for the exported data."""
    print("\n" + "="*70)
    print("STEP 3: GENERATING DOCUMENTATION")
    print("="*70)

    # Load the schema analysis
    analysis_file = output_dir / "json" / "schema_analysis.json"
    if not analysis_file.exists():
        print("No schema analysis found, skipping documentation")
        return

    with open(analysis_file, 'r') as f:
        analysis = json.load(f)

    # Create README
    readme_content = f"""# Structured Data Export

Generated by AI-Powered Web Scraper
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Source Information

- **Source URL**: {args.url}
- **Pages Crawled**: {args.max_pages} (max)
- **Crawl Depth**: {args.max_depth}
- **AI Provider**: {args.provider}

## Data Structure

### Content Type
{analysis.get('content_type', 'Unknown')}

### Entities
{chr(10).join(f"- {entity}" for entity in analysis.get('entities', []))}

### JSON Schema

```json
{json.dumps(analysis.get('schema', {}), indent=2)}
```

## Database Integration

### Recommended Indexes

The following fields should be indexed for optimal search performance:

{chr(10).join(f"- `{idx}`" for idx in analysis.get('indexes', []))}

### Loading into Database

#### MongoDB Example

```javascript
// Load the JSON file
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('{output_file.name}', 'utf8'));

// Insert into MongoDB
const MongoClient = require('mongodb').MongoClient;
const client = await MongoClient.connect('mongodb://localhost:27017');
const db = client.db('mydb');
const collection = db.collection('scraped_data');

await collection.insertMany(data);

// Create indexes
{chr(10).join(f"await collection.createIndex({{ {idx}: 1 }});" for idx in analysis.get('indexes', []))}
```

#### PostgreSQL Example (with JSONB)

```sql
-- Create table
CREATE TABLE scraped_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Load data (using COPY or INSERT)
-- Then create GIN index for JSONB
CREATE INDEX idx_scraped_data_gin ON scraped_data USING GIN (data);

-- Query examples
SELECT * FROM scraped_data WHERE data->>'field_name' = 'value';
SELECT * FROM scraped_data WHERE data @> '{{"key": "value"}}';
```

#### SQLite Example

```python
import sqlite3
import json

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE scraped_data (
        id INTEGER PRIMARY KEY,
        data TEXT,
        source_url TEXT
    )
''')

# Load and insert data
with open('{output_file.name}', 'r') as f:
    data = json.load(f)
    for item in data:
        cursor.execute(
            'INSERT INTO scraped_data (data, source_url) VALUES (?, ?)',
            (json.dumps(item), item.get('_metadata', {{}}).get('source_url'))
        )

conn.commit()

# Enable FTS (Full Text Search)
cursor.execute('CREATE VIRTUAL TABLE scraped_data_fts USING fts5(content)')
```

## Files Generated

- `{output_file}` - Structured JSON data
- `{analysis_file}` - Schema analysis and metadata
- `{output_dir / 'html'}/*.html` - Raw HTML files
- `{output_dir / 'json'}/scraped_data.json` - Raw scraped data
- `{output_dir / 'json'}/crawl_progress.json` - Crawl progress info

## Notes

{analysis.get('notes', 'No additional notes')}

## Search and Query Examples

### Full-Text Search

```python
# Example: Search across all text content
import json

with open('{output_file.name}', 'r') as f:
    data = json.load(f)

def search(query):
    results = []
    for item in data:
        # Search in relevant fields based on your schema
        if query.lower() in str(item).lower():
            results.append(item)
    return results

results = search("your search term")
```

### Filter by Metadata

```python
# Filter by source URL pattern
filtered = [item for item in data
           if 'pattern' in item.get('_metadata', {{}}).get('source_url', '')]
```

---

For more information about the web scraper tool, see the main README.md
"""

    readme_file = output_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"\nDocumentation generated: {readme_file}")


async def main():
    """Main entry point."""
    args = parse_arguments()

    print(f"\nAI-Powered Web Scraper - Data Retrieval Mode")
    print(f"{'='*70}\n")
    print(f"Target URL: {args.url}")
    print(f"Output Directory: {args.output_dir}")
    print(f"AI Provider: {args.provider}")
    print()

    try:
        # Step 1: Crawl website
        output_dir, scraped_data = await crawl_website(args)

        if not scraped_data:
            print("\nERROR: No data was scraped. Please check the URL and try again.")
            sys.exit(1)

        # Step 2: Convert to JSON (unless skipped)
        if args.skip_conversion:
            print("\nSkipping AI conversion (--skip-conversion flag set)")
            output_file = output_dir / "json" / "scraped_data.json"
            print(f"\nRaw data saved to: {output_file}")
        else:
            output_file = convert_to_json(args, output_dir, scraped_data)
            print(f"\nStructured data saved to: {output_file}")

            # Step 3: Generate documentation
            generate_documentation(output_dir, output_file, args)

        # Final summary
        print("\n" + "="*70)
        print("COMPLETE!")
        print("="*70)
        print(f"\nPages crawled: {len(scraped_data)}")
        print(f"Output file: {output_file}")
        print(f"Documentation: {output_dir / 'README.md'}")
        print("\nYour data is ready to be loaded into a database!")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
