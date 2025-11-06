#!/bin/bash
#
# SSA Blue Book Crawler Configuration
# Example script for crawling the SSA Disability Blue Book for Adults
#

# Set your API keys (choose one or more providers)
export GOOGLE_API_KEY="your-gemini-api-key-here"
# export ANTHROPIC_API_KEY="your-claude-api-key-here"
# export OPENAI_API_KEY="your-openai-api-key-here"

# SSA Blue Book URL
SSA_BLUEBOOK_URL="https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm"

# Run the scraper with SSA Blue Book specific settings
python ../scrape_to_json.py "$SSA_BLUEBOOK_URL" \
    --max-depth 3 \
    --max-pages 200 \
    --delay 2.0 \
    --provider gemini \
    --conversion-delay 2.0 \
    --output ssa_bluebook.json \
    --output-dir ./ssa_bluebook_data \
    --include "/disability/" \
    --include "/bluebook/"

echo ""
echo "SSA Blue Book data has been scraped and converted to JSON!"
echo "Output: ./ssa_bluebook.json"
echo "Documentation: ./ssa_bluebook_data/README.md"
