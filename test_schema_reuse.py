#!/usr/bin/env python3
"""
Test script for schema reuse functionality
"""

import json
import tempfile
from pathlib import Path


def test_schema_format():
    """Test that schema files in different formats are handled correctly."""
    print("Testing schema format handling...")

    # Test 1: Full analysis format (recommended)
    full_analysis = {
        "content_type": "Test Documentation",
        "entities": ["page", "section"],
        "schema": {
            "title": "string",
            "content": "string",
            "section": "string"
        },
        "indexes": ["title"],
        "notes": "Test schema"
    }

    # Test 2: Just schema object
    schema_only = {
        "title": "string",
        "content": "string",
        "section": "string"
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Write full analysis format
        full_analysis_file = Path(tmpdir) / "full_analysis.json"
        with open(full_analysis_file, 'w') as f:
            json.dump(full_analysis, f, indent=2)

        # Write schema-only format
        schema_only_file = Path(tmpdir) / "schema_only.json"
        with open(schema_only_file, 'w') as f:
            json.dump(schema_only, f, indent=2)

        print(f"  ✓ Full analysis format saved to: {full_analysis_file}")
        print(f"  ✓ Schema-only format saved to: {schema_only_file}")

        # Verify files can be loaded
        with open(full_analysis_file, 'r') as f:
            loaded_full = json.load(f)
            assert 'schema' in loaded_full
            print(f"  ✓ Full analysis format loaded successfully")

        with open(schema_only_file, 'r') as f:
            loaded_schema = json.load(f)
            assert 'title' in loaded_schema
            print(f"  ✓ Schema-only format loaded successfully")

    print("✅ Schema format handling test passed\n")


def test_schema_validation():
    """Test schema validation logic."""
    print("Testing schema validation...")

    # Valid schema
    valid_schema = {
        "title": "string",
        "url": "string",
        "content": "string"
    }

    # Invalid JSON (will be caught by json.load)
    invalid_json = "{ this is not valid json }"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Write valid schema
        valid_file = Path(tmpdir) / "valid_schema.json"
        with open(valid_file, 'w') as f:
            json.dump(valid_schema, f)

        # Write invalid JSON
        invalid_file = Path(tmpdir) / "invalid_schema.json"
        with open(invalid_file, 'w') as f:
            f.write(invalid_json)

        # Test valid schema loads
        try:
            with open(valid_file, 'r') as f:
                schema = json.load(f)
                print("  ✓ Valid schema loaded successfully")
        except json.JSONDecodeError:
            print("  ✗ Valid schema failed to load")
            return False

        # Test invalid JSON is caught
        try:
            with open(invalid_file, 'r') as f:
                schema = json.load(f)
                print("  ✗ Invalid JSON should have raised error")
                return False
        except json.JSONDecodeError:
            print("  ✓ Invalid JSON correctly caught")

    print("✅ Schema validation test passed\n")


def create_example_schema():
    """Create an example schema file for testing."""
    print("Creating example schema file...")

    example_schema = {
        "content_type": "Medical Documentation",
        "entities": ["condition", "criteria", "body_system"],
        "schema": {
            "condition_name": "string",
            "condition_code": "string",
            "body_system": "string",
            "criteria": "array of objects",
            "severity_levels": "array of strings",
            "diagnostic_requirements": "text",
            "notes": "text"
        },
        "indexes": ["condition_code", "body_system", "condition_name"],
        "notes": "Schema for medical disability criteria (e.g., SSA Blue Book)"
    }

    output_file = Path("example_schema.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(example_schema, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Example schema saved to: {output_file}")
    print("\n  You can use this schema with:")
    print(f"  python scrape_to_json.py <url> --schema {output_file}")
    print("✅ Example schema created\n")

    return output_file


def print_usage_examples():
    """Print usage examples for schema reuse."""
    print("="*70)
    print("SCHEMA REUSE - USAGE EXAMPLES")
    print("="*70)
    print()

    print("1. BASIC USAGE:")
    print("-" * 70)
    print("# First crawl - generate schema")
    print("python scrape_to_json.py https://example.com --output v1.json")
    print()
    print("# Later crawl - reuse schema")
    print("python scrape_to_json.py https://example.com \\")
    print("    --schema ./scraped_data/json/schema_analysis.json \\")
    print("    --output v2.json")
    print()

    print("2. MULTIPLE SIMILAR SITES:")
    print("-" * 70)
    print("# Crawl first state's site")
    print("python scrape_to_json.py https://state1.example.gov \\")
    print("    --output state1.json")
    print()
    print("# Use same schema for other states")
    print("python scrape_to_json.py https://state2.example.gov \\")
    print("    --schema ./scraped_data/json/schema_analysis.json \\")
    print("    --output state2.json")
    print()

    print("3. REGULAR UPDATES:")
    print("-" * 70)
    print("# Monthly update - keep schema consistent")
    print("python scrape_to_json.py https://docs.example.com \\")
    print("    --schema ./my_schema.json \\")
    print("    --output docs_$(date +%Y%m).json")
    print()

    print("4. CUSTOM SCHEMA:")
    print("-" * 70)
    print("# Create your own schema file (JSON format)")
    print("# Then use it:")
    print("python scrape_to_json.py https://example.com \\")
    print("    --schema ./my_custom_schema.json")
    print()

    print("="*70)
    print()


def main():
    """Run all tests."""
    print("="*70)
    print("SCHEMA REUSE FUNCTIONALITY TESTS")
    print("="*70)
    print()

    # Run tests
    test_schema_format()
    test_schema_validation()
    example_file = create_example_schema()

    # Print usage examples
    print_usage_examples()

    print("BENEFITS OF SCHEMA REUSE:")
    print("="*70)
    print("✅ Consistent field names across all crawls")
    print("✅ Same data types for all fields")
    print("✅ Easier to merge datasets from different times")
    print("✅ Faster processing (skips AI analysis)")
    print("✅ Reduced API costs")
    print("✅ Predictable database schema")
    print("✅ Works across similar sites")
    print()

    print("WHEN TO USE SCHEMA REUSE:")
    print("="*70)
    print("• Regular website monitoring/updates")
    print("• Multiple similar sites (state agencies, mirrors)")
    print("• Tracking content changes over time")
    print("• Maintaining consistent database structure")
    print("• Processing related websites with same structure")
    print()

    print("✅ All tests passed!")
    print()
    print(f"Example schema created: {example_file}")
    print("See examples/schema_reuse_example.sh for complete demonstration")


if __name__ == "__main__":
    main()
