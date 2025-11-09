#!/usr/bin/env python3
"""
Salvage Script for Existing Scraped Data

This script can convert existing scraped data to structured JSON,
even if the original conversion failed or was incomplete.

Usage:
    python salvage_scraped_data.py <path_to_scraped_data.json> [options]
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from ai_converter import AIDataConverter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Salvage and convert existing scraped data to structured JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert with Gemini
  python salvage_scraped_data.py ./scraped_data/json/scraped_data.json

  # Convert with Claude
  python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider claude

  # Use existing schema
  python salvage_scraped_data.py ./scraped_data/json/scraped_data.json \\
      --schema ./my_schema.json \\
      --output bluebook_final.json

  # Convert with Grok
  python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider grok
        """
    )

    parser.add_argument(
        "input_file",
        help="Path to the scraped_data.json file"
    )

    parser.add_argument(
        "--provider",
        choices=["gemini", "claude", "openai", "grok"],
        default="gemini",
        help="AI provider for data conversion (default: gemini)"
    )

    parser.add_argument(
        "--schema",
        type=str,
        help="Path to existing schema JSON file (optional)"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output JSON file path (default: auto-generated)"
    )

    parser.add_argument(
        "--conversion-delay",
        type=float,
        default=2.0,
        help="Delay between AI API calls in seconds (default: 2.0)"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of pages to process before saving progress (default: 5)"
    )

    return parser.parse_args()


def load_scraped_data(input_file: str):
    """Load scraped data from JSON file."""
    print(f"Loading scraped data from: {input_file}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("ERROR: Scraped data must be a list of page objects")
            return None

        print(f"✓ Loaded {len(data)} pages")
        return data

    except FileNotFoundError:
        print(f"ERROR: File not found: {input_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in file: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Failed to load file: {e}")
        return None


def load_schema(schema_file: str):
    """Load schema from JSON file."""
    print(f"\nLoading schema from: {schema_file}")

    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_data = json.load(f)

        # If the file contains a full analysis with 'schema' key, extract it
        if 'schema' in schema_data:
            analysis = schema_data
            print("✓ Loaded schema from analysis file")
        else:
            # Otherwise, assume the file is the schema itself
            analysis = {
                'content_type': 'Provided schema',
                'entities': [],
                'schema': schema_data,
                'indexes': [],
                'notes': 'Schema provided by user for salvage operation'
            }
            print("✓ Loaded schema directly from file")

        return analysis

    except FileNotFoundError:
        print(f"ERROR: Schema file not found: {schema_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in schema file: {e}")
        return None


def salvage_data(args, scraped_data):
    """Convert scraped data to structured JSON."""
    print("\n" + "="*70)
    print("SALVAGING SCRAPED DATA")
    print("="*70)

    # Initialize AI converter
    print(f"\nInitializing {args.provider} AI provider...")
    try:
        converter = AIDataConverter(provider=args.provider)
    except Exception as e:
        print(f"ERROR: Failed to initialize AI provider: {e}")
        print("\nMake sure you have set the appropriate API key:")
        print("  - Gemini: export GOOGLE_API_KEY=your-key")
        print("  - Claude: export ANTHROPIC_API_KEY=your-key")
        print("  - OpenAI: export OPENAI_API_KEY=your-key")
        print("  - Grok: export XAI_API_KEY=your-key")
        return None

    # Load or generate schema
    if args.schema:
        analysis = load_schema(args.schema)
        if not analysis:
            print("\nFalling back to automatic schema generation...")
            analysis = converter.analyze_data_structure(scraped_data)
    else:
        print("\nAnalyzing data structure...")
        analysis = converter.analyze_data_structure(scraped_data)

        print(f"\nData Analysis:")
        print(f"  Content Type: {analysis.get('content_type', 'Unknown')}")
        print(f"  Entities: {', '.join(analysis.get('entities', []))}")

    schema = analysis.get('schema', {})

    if not schema:
        print("\nERROR: No schema was generated or provided")
        return None

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        input_path = Path(args.input_file)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = input_path.parent / f"salvaged_data_{timestamp}.json"

    # Save schema for reference
    schema_output = output_file.parent / f"{output_file.stem}_schema.json"
    with open(schema_output, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"  Schema saved to: {schema_output}")

    # Convert all pages
    print(f"\nConverting {len(scraped_data)} pages to structured JSON...")
    print(f"Output will be saved to: {output_file}")

    structured_data = converter.convert_all_pages(
        scraped_data,
        schema,
        str(output_file),
        batch_size=args.batch_size,
        delay=args.conversion_delay
    )

    return output_file


def main():
    """Main entry point."""
    args = parse_arguments()

    print("="*70)
    print("SCRAPED DATA SALVAGE TOOL")
    print("="*70)
    print()

    # Load scraped data
    scraped_data = load_scraped_data(args.input_file)
    if not scraped_data:
        sys.exit(1)

    # Show some statistics
    print(f"\nData Statistics:")
    print(f"  Total pages: {len(scraped_data)}")

    if scraped_data:
        sample_page = scraped_data[0]
        print(f"  First page URL: {sample_page.get('url', 'Unknown')}")
        print(f"  First page title: {sample_page.get('title', 'Unknown')}")

        # Count pages with tables
        pages_with_tables = sum(1 for page in scraped_data if page.get('tables'))
        print(f"  Pages with tables: {pages_with_tables}")

        # Count total headings
        total_headings = sum(len(page.get('headings', [])) for page in scraped_data)
        print(f"  Total headings: {total_headings}")

    # Salvage the data
    output_file = salvage_data(args, scraped_data)

    if output_file:
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(f"\nStructured data saved to: {output_file}")
        print(f"Schema saved to: {output_file.parent / f'{output_file.stem}_schema.json'}")
        print("\nYour data is now ready to be loaded into a database!")
    else:
        print("\n" + "="*70)
        print("FAILED")
        print("="*70)
        print("\nSalvage operation failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
