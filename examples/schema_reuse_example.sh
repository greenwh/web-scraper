#!/bin/bash
#
# Schema Reuse Example
# Demonstrates how to use a schema from a previous crawl for consistent parsing
#

# Set your API key
export GOOGLE_API_KEY="your-gemini-api-key-here"

# Example: Medical website that gets updated regularly
# You want to maintain consistent schema across updates

echo "=========================================="
echo "INITIAL CRAWL - Generate Schema"
echo "=========================================="

# First crawl: Generate schema automatically
python ../scrape_to_json.py "https://example-medical-site.org" \
    --max-depth 2 \
    --max-pages 50 \
    --output initial_data.json \
    --output-dir ./medical_data_v1

echo ""
echo "Schema generated at: ./medical_data_v1/json/schema_analysis.json"
echo ""
echo "Press Enter to continue with schema reuse example..."
read

echo "=========================================="
echo "SUBSEQUENT CRAWL - Reuse Schema"
echo "=========================================="

# Later: Site has been updated, you want to recrawl with the same schema
python ../scrape_to_json.py "https://example-medical-site.org" \
    --max-depth 2 \
    --max-pages 50 \
    --schema ./medical_data_v1/json/schema_analysis.json \
    --output updated_data.json \
    --output-dir ./medical_data_v2

echo ""
echo "=========================================="
echo "BENEFITS OF SCHEMA REUSE:"
echo "=========================================="
echo ""
echo "✅ Consistent field names across versions"
echo "✅ Same data types for all fields"
echo "✅ Easier to merge or compare datasets"
echo "✅ Faster processing (skips schema analysis)"
echo "✅ Predictable database schema"
echo ""
echo "Use cases:"
echo "  - Regular site updates/monitoring"
echo "  - Multiple similar sites (e.g., different state agencies)"
echo "  - Version control of website content"
echo "  - Incremental data collection"
echo ""

# Advanced: Use the same schema for multiple related sites
echo "=========================================="
echo "ADVANCED: Multiple Sites, Same Schema"
echo "=========================================="
echo ""
echo "# Use the schema from Site 1 for Site 2"
echo "python ../scrape_to_json.py https://site2.example.org \\"
echo "    --schema ./medical_data_v1/json/schema_analysis.json \\"
echo "    --output site2_data.json"
echo ""
echo "# This works well for:"
echo "  - State/regional variations of same content"
echo "  - Mirror sites"
echo "  - Multi-language versions"
echo ""
