# AI-Powered Web Scraper

A powerful Python tool for intelligent web scraping with two operational modes: **interactive browsing** and **automated data retrieval**.

## 🌟 Key Features

- **🤖 Multi-AI Support**: Works with Gemini, Claude, and OpenAI
- **🌐 JavaScript Support**: Full browser automation via Playwright
- **📦 Offline Storage**: Save websites for offline analysis
- **🗃️ Database-Ready JSON**: Auto-generated schemas for easy database integration
- **🔄 Schema Reuse**: Use existing schemas for consistent parsing across runs
- **🎯 Smart Filtering**: Include/exclude URL patterns, domain restrictions
- **📊 Structured Data**: Handles both textual and tabular content
- **📝 Auto Documentation**: Generates README with database examples
- **⚡ Progress Tracking**: Resume interrupted crawls

## 🚀 Quick Start

**1. Install:**
```bash
# System dependencies (if needed)
sudo apt-get install libnspr4 libnss3 libasound2t64

# Python dependencies
pip install -r requirements.txt
playwright install chromium
```

**2. Set API Key:**
```bash
export GOOGLE_API_KEY="your-key"  # or ANTHROPIC_API_KEY or OPENAI_API_KEY
```

**3. Run:**
```bash
# Interactive mode
python main.py

# Data retrieval mode
python scrape_to_json.py https://example.com
```

👉 **New user?** See [QUICKSTART.md](QUICKSTART.md) for detailed setup guide!

## 📋 Two Modes of Operation

### Mode 1: Interactive Browsing 🖱️

Browse websites with real-time AI summaries:

```bash
python main.py
```

- Navigate through websites interactively
- Get AI summaries of each page
- Handle login-required sites
- Follow links or enter new URLs

### Mode 2: Data Retrieval & JSON Export 📊

Crawl entire websites and export to structured JSON:

```bash
python scrape_to_json.py <url> [options]
```

**Perfect for:**
- Creating offline documentation databases
- Archiving medical/legal resources (e.g., SSA Blue Book)
- Extracting product catalogs
- Building searchable knowledge bases

## 🎯 Primary Use Case: SSA Blue Book

Retrieve the complete Social Security Disability Blue Book as structured JSON:

```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --output ssa_bluebook.json
```

**Output:** Database-ready JSON with:
- Impairment codes and categories
- Body system classifications
- Medical criteria and requirements
- Searchable and indexable structure

See `examples/ssa_bluebook_config.sh` for full configuration.

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute setup guide for beginners |
| **[DATA_RETRIEVAL_README.md](DATA_RETRIEVAL_README.md)** | Complete guide for data retrieval mode |
| **[CLAUDE.md](CLAUDE.md)** | Technical architecture and API reference |

## 💡 Usage Examples

### Example 1: Simple Documentation Site

```bash
python scrape_to_json.py https://docs.example.com \
    --max-depth 2 \
    --max-pages 50 \
    --include "/docs/"
```

### Example 2: Medical Guidelines with Claude AI

```bash
python scrape_to_json.py https://medical-guidelines.org \
    --provider claude \
    --max-depth 3 \
    --delay 2.0
```

### Example 3: Product Catalog

```bash
python scrape_to_json.py https://shop.example.com \
    --include "/products/" \
    --exclude "/cart/" \
    --max-pages 500
```

### Example 4: Crawl Only (No AI Conversion)

```bash
python scrape_to_json.py https://example.com \
    --skip-conversion \
    --max-pages 100
```

### Example 5: Reuse Schema for Consistent Updates

```bash
# First crawl - generate schema
python scrape_to_json.py https://example.com --output v1.json

# Later - reuse schema for consistent structure
python scrape_to_json.py https://example.com \
    --schema ./scraped_data/json/schema_analysis.json \
    --output v2.json
```

## 🔧 Configuration Options

### Crawling Parameters

```bash
--max-depth 3           # How deep to follow links
--max-pages 100         # Maximum pages to crawl
--delay 2.0            # Seconds between requests
--same-domain          # Stay on same domain (default: true)
--include "/pattern/"  # Include URLs matching pattern
--exclude "/pattern/"  # Exclude URLs matching pattern
```

### AI Providers

```bash
--provider gemini      # Google Gemini (default, fast & cheap)
--provider claude      # Anthropic Claude (best for complex structures)
--provider openai      # OpenAI GPT (balanced)
--provider grok        # xAI Grok (alternative option)
--schema file.json     # Use existing schema for consistent parsing
```

### Output Options

```bash
--output file.json     # Output filename
--output-dir ./data    # Output directory
--skip-conversion      # Skip AI conversion (raw data only)
```

**See full options:** `python scrape_to_json.py --help`

## 📂 Output Structure

```
scraped_data/
├── html/                          # Raw HTML files
│   ├── abc123.html
│   └── def456.html
├── json/
│   ├── scraped_data.json         # Raw extracted data
│   ├── schema_analysis.json      # AI-generated schema
│   └── crawl_progress.json       # Progress tracking
├── structured_data_*.json         # ⭐ YOUR FINAL DATABASE-READY JSON
└── README.md                      # Auto-generated documentation
```

## 💾 Database Integration

The tool generates database-ready JSON. Here's how to load it:

### MongoDB
```javascript
const data = require('./structured_data.json');
await db.collection.insertMany(data);
```

### PostgreSQL (JSONB)
```sql
CREATE TABLE my_data (id SERIAL, data JSONB);
-- Load using COPY or pg_import
```

### SQLite
```python
import json, sqlite3
conn = sqlite3.connect('mydb.db')
data = json.load(open('structured_data.json'))
# Insert data...
```

**Full examples** in the auto-generated README.md in your output directory!

## 🧪 Testing

Run the test suite to verify installation:

```bash
python test_modules.py
```

## 📞 Support

- 📖 **Full Documentation**: See [DATA_RETRIEVAL_README.md](DATA_RETRIEVAL_README.md)
- 🚀 **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- 🏗️ **Technical Details**: See [CLAUDE.md](CLAUDE.md)

---

**Ready to get started?** → [QUICKSTART.md](QUICKSTART.md)