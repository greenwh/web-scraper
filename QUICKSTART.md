# Quick Start Guide - Website Data Retrieval

Get started with website data retrieval and JSON export in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An API key for at least one AI provider:
  - [Google Gemini](https://makersuite.google.com/app/apikey) (recommended - free tier available)
  - [Anthropic Claude](https://console.anthropic.com/)
  - [OpenAI](https://platform.openai.com/api-keys)

## Installation (5 steps)

### 1. Clone/Download the Project

```bash
cd /path/to/web-scraper
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Browser

```bash
playwright install chromium
```

### 5. Set API Key

```bash
# For Gemini (recommended for getting started)
export GOOGLE_API_KEY="your-api-key-here"

# Or for Claude
export ANTHROPIC_API_KEY="your-api-key-here"

# Or for OpenAI
export OPENAI_API_KEY="your-api-key-here"
```

**Pro tip:** Add the export to your `~/.bashrc` or `~/.zshrc` to make it permanent.

## Your First Crawl

### Example 1: Simple Website

```bash
python scrape_to_json.py https://example.com \
    --max-depth 1 \
    --max-pages 10
```

This will:
- Crawl up to 10 pages from example.com
- Extract content and structure
- Generate structured JSON
- Create documentation

Output will be in `./scraped_data/`

### Example 2: SSA Blue Book (Primary Use Case)

```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --output ssa_bluebook.json
```

This retrieves the complete SSA Disability Blue Book as structured JSON ready for database loading.

### Example 3: Custom Configuration

```bash
python scrape_to_json.py https://docs.example.com \
    --max-depth 2 \
    --max-pages 50 \
    --delay 2.0 \
    --provider claude \
    --include "/documentation/" \
    --exclude "/archive/" \
    --output my_docs.json
```

## Understanding the Output

After running, you'll find:

```
scraped_data/
├── html/                         # Raw HTML files (for reference)
├── json/
│   ├── scraped_data.json        # Raw scraped data
│   ├── schema_analysis.json     # AI-generated schema
│   └── crawl_progress.json      # Progress tracking
├── structured_data_*.json        # YOUR FINAL OUTPUT (load this into DB)
└── README.md                     # Documentation for your data
```

The most important file is **`structured_data_*.json`** - this is your database-ready JSON.

## Loading into a Database

### MongoDB

```javascript
const data = require('./scraped_data/structured_data_20240101.json');
db.collection.insertMany(data);
```

### PostgreSQL (JSONB)

```sql
CREATE TABLE my_data (id SERIAL, data JSONB);
-- Then use COPY or pg_import with the JSON file
```

### SQLite

```python
import sqlite3
import json

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

with open('structured_data_20240101.json') as f:
    data = json.load(f)
    for item in data:
        cursor.execute('INSERT INTO my_table (data) VALUES (?)',
                      (json.dumps(item),))
conn.commit()
```

See the auto-generated `README.md` in your output directory for complete examples!

## Common Options

| Option | What it does | Example |
|--------|-------------|---------|
| `--max-depth 3` | How deep to crawl (links from links) | 1 = one page, 3 = three levels deep |
| `--max-pages 100` | Maximum pages to fetch | Prevents unlimited crawling |
| `--delay 2.0` | Seconds between requests | Be polite to servers |
| `--provider gemini` | Which AI to use | `gemini`, `claude`, or `openai` |
| `--output file.json` | Output filename | Default is auto-generated |
| `--include "/docs/"` | Only crawl URLs with this pattern | Can use multiple times |
| `--exclude "/blog/"` | Skip URLs with this pattern | Can use multiple times |

## Choosing an AI Provider

| Provider | Best For | Cost | Speed |
|----------|----------|------|-------|
| **Gemini** | Getting started, large crawls | 💰 Cheapest | ⚡ Fast |
| **Claude** | Complex structures, medical/legal | 💰💰 Mid | ⚡⚡ Good |
| **OpenAI** | Balanced use cases | 💰💰 Mid | ⚡⚡ Good |
| **Grok** | Alternative option | 💰💰 Mid | ⚡⚡ Good |

**Recommendation:** Start with Gemini, switch to Claude if you need higher accuracy for complex content.

## Pro Tip: Reuse Schemas for Consistency

Want consistent data structure across multiple crawls? Save and reuse your schema!

```bash
# First crawl - generates schema automatically
python scrape_to_json.py https://example.com --output v1.json

# Later crawl - reuse the schema for consistency
python scrape_to_json.py https://example.com \
    --schema ./scraped_data/json/schema_analysis.json \
    --output v2.json
```

**Benefits:**
- ✅ Same field names every time
- ✅ Easy to merge datasets
- ✅ Faster (skips AI analysis)
- ✅ Works for similar sites too!

**Perfect for:**
- Regular website monitoring
- Multiple similar sites (e.g., state agencies)
- Tracking changes over time

See `examples/schema_reuse_example.sh` for more details!

## Troubleshooting

### "No module named 'playwright'"

```bash
pip install playwright
playwright install chromium
```

### "GOOGLE_API_KEY environment variable not set"

```bash
export GOOGLE_API_KEY="your-key"
# Then run your command again
```

### "403 Forbidden" errors

Some sites block bots. Try:
- Increase delay: `--delay 3.0`
- Reduce pages: `--max-pages 20`
- Some sites just don't allow scraping - check their robots.txt

### Out of memory

Reduce scope:
- `--max-pages 50` (fewer pages)
- `--max-depth 2` (less deep)
- Process in smaller batches

## Next Steps

1. ✅ **You're ready!** Try crawling a simple site first
2. 📖 **Read more:** See `DATA_RETRIEVAL_README.md` for advanced usage
3. 🔧 **Customize:** Check `examples/ssa_bluebook_config.sh` for configuration examples
4. 💾 **Use your data:** Load JSON into your database using examples in the generated README.md

## Need Help?

- Full documentation: `DATA_RETRIEVAL_README.md`
- Technical details: `CLAUDE.md`
- Test the installation: `python test_modules.py`

## Quick Command Reference

```bash
# Minimal command
python scrape_to_json.py https://example.com

# Typical usage
python scrape_to_json.py https://example.com \
    --max-depth 2 \
    --max-pages 50

# Full control
python scrape_to_json.py https://example.com \
    --max-depth 3 \
    --max-pages 100 \
    --delay 2.0 \
    --provider claude \
    --output mydata.json \
    --include "/section/" \
    --exclude "/archive/"

# Just crawl, no AI conversion (faster)
python scrape_to_json.py https://example.com \
    --skip-conversion

# Get help
python scrape_to_json.py --help
```

Happy scraping! 🚀
