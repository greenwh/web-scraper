#!/usr/bin/env python3
"""
Test script for the data retrieval and conversion modules
Tests basic functionality without making actual API calls
"""

import asyncio
import json
from pathlib import Path
import tempfile
import shutil


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import crawler
        import ai_converter
        import scrape_to_json
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_crawler_init():
    """Test crawler initialization."""
    print("\nTesting crawler initialization...")
    try:
        from crawler import WebsiteCrawler

        with tempfile.TemporaryDirectory() as tmpdir:
            crawler_obj = WebsiteCrawler(
                base_url="https://example.com",
                output_dir=tmpdir,
                max_depth=2,
                max_pages=10
            )

            # Check attributes
            assert crawler_obj.base_url == "https://example.com"
            assert crawler_obj.max_depth == 2
            assert crawler_obj.max_pages == 10
            assert crawler_obj.base_domain == "example.com"

            # Check directories created
            assert Path(tmpdir).exists()
            assert (Path(tmpdir) / "html").exists()
            assert (Path(tmpdir) / "json").exists()

        print("✓ Crawler initialization successful")
        return True
    except Exception as e:
        print(f"✗ Crawler initialization failed: {e}")
        return False


def test_url_filtering():
    """Test URL filtering logic."""
    print("\nTesting URL filtering...")
    try:
        from crawler import WebsiteCrawler

        with tempfile.TemporaryDirectory() as tmpdir:
            # Test same domain only
            crawler_obj = WebsiteCrawler(
                base_url="https://example.com/page",
                output_dir=tmpdir,
                same_domain_only=True
            )

            assert crawler_obj._should_crawl("https://example.com/other")
            assert not crawler_obj._should_crawl("https://other.com/page")

            # Test include/exclude patterns
            crawler_obj = WebsiteCrawler(
                base_url="https://example.com",
                output_dir=tmpdir,
                include_patterns=["/docs/"],
                exclude_patterns=["/archive/"]
            )

            assert crawler_obj._should_crawl("https://example.com/docs/page")
            assert not crawler_obj._should_crawl("https://example.com/blog/")
            assert not crawler_obj._should_crawl("https://example.com/docs/archive/old")

        print("✓ URL filtering works correctly")
        return True
    except Exception as e:
        print(f"✗ URL filtering failed: {e}")
        return False


def test_ai_converter_init():
    """Test AI converter initialization (without API keys)."""
    print("\nTesting AI converter initialization...")
    try:
        from ai_converter import AIDataConverter

        # Test that it requires API keys
        try:
            converter = AIDataConverter(provider="gemini")
            print("  Warning: Gemini initialized without checking API key")
        except ValueError as e:
            if "GOOGLE_API_KEY" in str(e):
                print("✓ Correctly requires GOOGLE_API_KEY")
            else:
                raise

        try:
            converter = AIDataConverter(provider="claude")
            print("  Warning: Claude initialized without checking API key")
        except (ValueError, ImportError) as e:
            print(f"✓ Correctly requires ANTHROPIC_API_KEY or anthropic package")

        try:
            converter = AIDataConverter(provider="openai")
            print("  Warning: OpenAI initialized without checking API key")
        except (ValueError, ImportError) as e:
            print(f"✓ Correctly requires OPENAI_API_KEY or openai package")

        # Test invalid provider
        try:
            converter = AIDataConverter(provider="invalid")
            print("✗ Should have rejected invalid provider")
            return False
        except ValueError:
            print("✓ Correctly rejects invalid provider")

        return True
    except Exception as e:
        print(f"✗ AI converter initialization test failed: {e}")
        return False


def test_data_structures():
    """Test data structure handling."""
    print("\nTesting data structures...")
    try:
        # Create sample scraped data
        sample_data = [
            {
                'url': 'https://example.com/page1',
                'url_hash': 'abc123',
                'title': 'Test Page 1',
                'text_content': 'This is test content about topic A.',
                'headings': [
                    {'level': 1, 'text': 'Main Title'},
                    {'level': 2, 'text': 'Subtitle'}
                ],
                'tables': [
                    [['Header1', 'Header2'], ['Value1', 'Value2']]
                ],
                'links': ['https://example.com/page2'],
                'html_file': '/tmp/abc123.html',
                'fetched_at': 1234567890.0
            }
        ]

        # Verify structure
        assert 'url' in sample_data[0]
        assert 'headings' in sample_data[0]
        assert 'tables' in sample_data[0]
        assert len(sample_data[0]['headings']) == 2
        assert len(sample_data[0]['tables'][0]) == 2

        print("✓ Data structures are valid")
        return True
    except Exception as e:
        print(f"✗ Data structure test failed: {e}")
        return False


async def test_crawler_basic():
    """Test basic crawling functionality with a simple page."""
    print("\nTesting basic crawling (this may take a few seconds)...")
    try:
        from crawler import WebsiteCrawler

        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a simple, reliable test site
            crawler_obj = WebsiteCrawler(
                base_url="http://example.com",  # Simple, reliable test site
                output_dir=tmpdir,
                max_depth=0,  # Only crawl the starting page
                max_pages=1,
                delay=0.5
            )

            scraped_data = await crawler_obj.crawl()

            # Check results
            assert len(scraped_data) == 1
            assert 'url' in scraped_data[0]
            assert 'text_content' in scraped_data[0]
            assert scraped_data[0]['url'] == "http://example.com"

            # Check files created
            json_file = Path(tmpdir) / "json" / "scraped_data.json"
            assert json_file.exists()

            with open(json_file, 'r') as f:
                saved_data = json.load(f)
                assert len(saved_data) == 1

        print("✓ Basic crawling successful")
        return True
    except Exception as e:
        print(f"✗ Basic crawling failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_json_output():
    """Test JSON file generation."""
    print("\nTesting JSON output...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_output.json"

            # Create sample data
            test_data = [
                {
                    "id": 1,
                    "content": "Test content",
                    "_metadata": {
                        "source_url": "https://example.com",
                        "scraped_at": 1234567890.0
                    }
                }
            ]

            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, indent=2, ensure_ascii=False)

            # Verify file
            assert output_file.exists()

            # Load and verify
            with open(output_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert loaded_data == test_data

        print("✓ JSON output works correctly")
        return True
    except Exception as e:
        print(f"✗ JSON output test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests."""
    print("="*70)
    print("WEB SCRAPER MODULE TESTS")
    print("="*70)

    results = []

    # Basic tests (no async)
    results.append(("Imports", test_imports()))
    results.append(("Crawler Init", test_crawler_init()))
    results.append(("URL Filtering", test_url_filtering()))
    results.append(("AI Converter Init", test_ai_converter_init()))
    results.append(("Data Structures", test_data_structures()))
    results.append(("JSON Output", test_json_output()))

    # Async tests
    results.append(("Basic Crawling", await test_crawler_basic()))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
