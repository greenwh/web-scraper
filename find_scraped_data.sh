#!/bin/bash

# Script to help find scraped data files on your local machine

echo "========================================================================"
echo "FINDING SCRAPED DATA FILES"
echo "========================================================================"
echo ""

# Check current directory first
echo "1. Checking current directory..."
if [ -d "./scraped_data" ]; then
    echo "   ✓ Found scraped_data directory in current location"
    echo "   Location: $(pwd)/scraped_data"
    echo ""
    echo "   Contents:"
    ls -lah ./scraped_data/
    echo ""
    if [ -f "./scraped_data/json/scraped_data.json" ]; then
        echo "   ✓ Found scraped_data.json"
        echo "   Size: $(du -h ./scraped_data/json/scraped_data.json | cut -f1)"
        echo "   Pages: $(cat ./scraped_data/json/scraped_data.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "?")"
    fi
else
    echo "   ✗ No scraped_data directory in current location"
fi

echo ""
echo "2. Searching for scraped_data directories in common locations..."
echo ""

# Search home directory for scraped_data directories
find ~ -type d -name "scraped_data" 2>/dev/null | while read dir; do
    echo "   Found: $dir"
    if [ -f "$dir/json/scraped_data.json" ]; then
        echo "     ✓ Contains scraped_data.json"
        echo "     Size: $(du -h "$dir/json/scraped_data.json" | cut -f1)"
        pages=$(cat "$dir/json/scraped_data.json" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data))" 2>/dev/null || echo "?")
        echo "     Pages: $pages"
    fi
    echo ""
done

echo ""
echo "3. Searching for any .json files with 'ssa' or 'bluebook' in the name..."
echo ""

find ~ -type f \( -name "*ssa*.json" -o -name "*bluebook*.json" -o -name "*blue_book*.json" \) 2>/dev/null | while read file; do
    echo "   Found: $file"
    echo "   Size: $(du -h "$file" | cut -f1)"
    echo "   Modified: $(stat -c %y "$file" 2>/dev/null || stat -f "%Sm" "$file" 2>/dev/null)"
    echo ""
done

echo ""
echo "4. Searching for large JSON files (might be scraped data)..."
echo ""

find ~ -type f -name "*.json" -size +100k 2>/dev/null | head -10 | while read file; do
    echo "   Found: $file"
    echo "   Size: $(du -h "$file" | cut -f1)"
    echo ""
done

echo ""
echo "========================================================================"
echo "SEARCH COMPLETE"
echo "========================================================================"
echo ""
echo "If you found scraped data, you can salvage it using:"
echo ""
echo "  python salvage_scraped_data.py <path_to_scraped_data.json>"
echo ""
echo "For example:"
echo "  python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider gemini"
echo ""
echo "If no data was found, you may need to run the scraper again:"
echo "  python scrape_to_json.py https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \\"
echo "      --max-depth 3 --max-pages 200 --provider gemini"
echo ""
