# Website Data Retrieval and JSON Export

This module extends the AI-Powered Web Scraper with offline data retrieval capabilities (similar to `wget -m` or HTTrack) and AI-powered conversion to structured JSON for database integration.

## Features

### 1. Recursive Website Crawling
- **Deep crawling**: Configurable depth and page limits
- **Offline storage**: Saves HTML and extracted content locally
- **Smart filtering**: Include/exclude URL patterns
- **Rate limiting**: Polite crawling with configurable delays
- **Progress tracking**: Incremental saves and resume capability

### 2. AI-Powered JSON Conversion
- **Multi-AI support**: Works with Claude (Anthropic), Gemini (Google), or OpenAI
- **Automatic schema generation**: AI analyzes content and creates optimal database schema
- **Handles diverse content**: Both textual and tabular data
- **Metadata preservation**: Tracks source URLs, timestamps, and more
- **Batch processing**: Efficient processing with progress saves

### 3. Database-Ready Output
- **Structured JSON**: Clean, consistent data structure
- **Schema documentation**: Detailed field descriptions
- **Index recommendations**: Optimized for search performance
- **Integration examples**: MongoDB, PostgreSQL, SQLite examples

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Set up API keys (choose one or more)
export GOOGLE_API_KEY="your-key"          # For Gemini
export ANTHROPIC_API_KEY="your-key"       # For Claude
export OPENAI_API_KEY="your-key"          # For OpenAI
```

## Quick Start

### Basic Usage

```bash
# Crawl a website and convert to JSON
python scrape_to_json.py https://example.com

# Customize crawling parameters
python scrape_to_json.py https://example.com \
    --max-depth 2 \
    --max-pages 50 \
    --delay 2.0 \
    --provider claude \
    --output mydata.json
```

### SSA Blue Book Example

This is the primary use case - retrieving the complete SSA Disability Blue Book:

```bash
# Option 1: Using the example script
cd examples
chmod +x ssa_bluebook_config.sh
./ssa_bluebook_config.sh

# Option 2: Direct command
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --delay 2.0 \
    --provider gemini \
    --output ssa_bluebook.json \
    --include "/disability/" \
    --include "/bluebook/"
```

This will:
1. Crawl all pages in the SSA Blue Book section
2. Extract structured information (body systems, impairments, criteria)
3. Generate a JSON file with searchable disability listings
4. Create schema documentation for database integration

## Command-Line Options

### Crawling Options

| Option | Default | Description |
|--------|---------|-------------|
| `--max-depth` | 3 | Maximum depth for recursive crawling |
| `--max-pages` | 100 | Maximum number of pages to crawl |
| `--delay` | 1.0 | Delay between requests (seconds) |
| `--same-domain` | True | Only crawl URLs from same domain |
| `--include` | None | Include URLs matching pattern (multiple allowed) |
| `--exclude` | None | Exclude URLs matching pattern (multiple allowed) |

### AI Conversion Options

| Option | Default | Description |
|--------|---------|-------------|
| `--provider` | gemini | AI provider: `gemini`, `claude`, or `openai` |
| `--skip-conversion` | False | Skip AI conversion, save raw data only |
| `--conversion-delay` | 2.0 | Delay between AI API calls (seconds) |
| `--schema` | None | Path to existing schema JSON for consistent parsing |

### Output Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | Auto | Output JSON file path |
| `--output-dir` | ./scraped_data | Directory for all scraped data |

## Architecture

### Module Overview

```
scrape_to_json.py       # Main integration script
    ├── crawler.py      # Website crawling module
    └── ai_converter.py # AI-powered JSON conversion

main.py                 # Original interactive scraper (still available)
```

### Data Flow

```
1. CRAWLING
   URL → Playwright → BeautifulSoup → Extract content
                                    → Extract links
                                    → Extract tables
                                    → Save HTML
                                    ↓
                              Raw JSON data

2. AI ANALYSIS
   Raw data → AI Provider → Analyze structure
                         → Generate schema
                         → Identify entities
                         ↓
                    Schema + Analysis

3. CONVERSION
   Raw data + Schema → AI Provider → Convert each page
                                   → Add metadata
                                   ↓
                            Structured JSON

4. DOCUMENTATION
   Schema + Analysis → Generate README
                    → Database examples
                    → Index recommendations
```

## Output Structure

After running the tool, you'll get:

```
scraped_data/
├── html/                          # Raw HTML files
│   ├── abc123.html
│   └── def456.html
├── json/
│   ├── scraped_data.json         # Raw scraped data
│   ├── crawl_progress.json       # Progress tracking
│   └── schema_analysis.json      # AI-generated schema
├── structured_data_YYYYMMDD.json # Final structured JSON
└── README.md                      # Documentation
```

## AI Providers

### Gemini (Google) - Default

```bash
export GOOGLE_API_KEY="your-key"
python scrape_to_json.py https://example.com --provider gemini
```

**Pros**: Fast, cost-effective, good general performance
**Best for**: Large-scale crawling, general content

### Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="your-key"
python scrape_to_json.py https://example.com --provider claude
```

**Pros**: Excellent understanding of complex structures, very accurate
**Best for**: Technical documentation, complex hierarchies, legal/medical text

### OpenAI (GPT)

```bash
export OPENAI_API_KEY="your-key"
python scrape_to_json.py https://example.com --provider openai
```

**Pros**: Good balance of speed and accuracy
**Best for**: Mixed content, varied structures

## Working with Different Content Types

### Technical Documentation

```bash
python scrape_to_json.py https://docs.example.com \
    --max-depth 4 \
    --include "/docs/" \
    --exclude "/blog/" \
    --provider claude
```

### E-commerce/Product Catalogs

```bash
python scrape_to_json.py https://shop.example.com \
    --max-depth 2 \
    --max-pages 500 \
    --include "/products/" \
    --provider gemini
```

### Medical/Legal Resources (like SSA Blue Book)

```bash
python scrape_to_json.py https://medical.example.com \
    --max-depth 3 \
    --delay 2.0 \
    --conversion-delay 2.0 \
    --provider claude  # Claude excels at structured professional content
```

### News/Blog Archives

```bash
python scrape_to_json.py https://blog.example.com \
    --max-depth 2 \
    --include "/202" \  # Include year patterns
    --provider gemini
```

## Database Integration

### MongoDB

```javascript
const fs = require('fs');
const { MongoClient } = require('mongodb');

async function loadData() {
    const data = JSON.parse(fs.readFileSync('ssa_bluebook.json'));
    const client = await MongoClient.connect('mongodb://localhost:27017');
    const db = client.db('ssa');
    const collection = db.collection('bluebook');

    await collection.insertMany(data);

    // Create indexes for search
    await collection.createIndex({ '_metadata.title': 'text' });
    await collection.createIndex({ 'impairment_code': 1 });

    // Full-text search
    const results = await collection.find({
        $text: { $search: 'neurological disorders' }
    }).toArray();

    console.log(`Found ${results.length} results`);
}
```

### PostgreSQL with JSONB

```sql
-- Create table
CREATE TABLE bluebook (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    source_url TEXT,
    impairment_code TEXT GENERATED ALWAYS AS (data->>'impairment_code') STORED
);

-- Load data (example with psql)
\copy bluebook (data, source_url) FROM PROGRAM 'jq -c ".[] | {data: ., source_url: ._metadata.source_url}" ssa_bluebook.json' WITH (FORMAT csv, QUOTE e'\x01', DELIMITER e'\x02');

-- Create indexes
CREATE INDEX idx_bluebook_gin ON bluebook USING GIN (data);
CREATE INDEX idx_bluebook_code ON bluebook (impairment_code);

-- Query examples
SELECT * FROM bluebook WHERE data->>'body_system' = 'Neurological';
SELECT * FROM bluebook WHERE data @> '{"severity": "severe"}';
```

### SQLite with FTS5

```python
import sqlite3
import json

conn = sqlite3.connect('ssa_bluebook.db')
cursor = conn.cursor()

# Create table with FTS
cursor.execute('''
    CREATE VIRTUAL TABLE bluebook USING fts5(
        impairment_code,
        body_system,
        description,
        criteria,
        source_url
    )
''')

# Load data
with open('ssa_bluebook.json', 'r') as f:
    data = json.load(f)
    for item in data:
        cursor.execute('''
            INSERT INTO bluebook VALUES (?, ?, ?, ?, ?)
        ''', (
            item.get('impairment_code'),
            item.get('body_system'),
            item.get('description'),
            json.dumps(item.get('criteria', [])),
            item['_metadata']['source_url']
        ))

conn.commit()

# Full-text search
results = cursor.execute('''
    SELECT * FROM bluebook WHERE bluebook MATCH 'respiratory disorders'
''').fetchall()
```

## Advanced Features

### Resume Interrupted Crawls

The crawler automatically saves progress. If interrupted, check:

```bash
# View progress
cat scraped_data/json/crawl_progress.json

# The crawler will skip already-visited URLs if you re-run
```

### Custom Filtering

```bash
# Only crawl specific sections
python scrape_to_json.py https://example.com \
    --include "/section1/" \
    --include "/section2/" \
    --exclude "/archive/" \
    --exclude "/comments/"
```

### Raw Data Only (No AI Conversion)

```bash
# For when you want to process data yourself
python scrape_to_json.py https://example.com --skip-conversion
```

### Schema Reuse for Consistent Parsing

One of the most powerful features is the ability to reuse schemas from previous crawls. This ensures consistent data structure across multiple runs or site updates.

**Why use schema reuse?**
- ✅ **Consistency**: Same field names and types across all crawls
- ✅ **Speed**: Skip AI analysis step (faster, cheaper)
- ✅ **Mergeability**: Easy to combine data from multiple runs
- ✅ **Version Control**: Track website changes over time
- ✅ **Multi-site**: Apply same schema to similar sites

**Basic usage:**

```bash
# First crawl - generate schema
python scrape_to_json.py https://example.com \
    --output initial_data.json \
    --output-dir ./data_v1

# Save the schema for reuse
cp ./data_v1/json/schema_analysis.json ./my_schema.json

# Later crawl - reuse schema
python scrape_to_json.py https://example.com \
    --schema ./my_schema.json \
    --output updated_data.json \
    --output-dir ./data_v2
```

**Advanced: Multi-site with same schema**

```bash
# Generate schema from Site 1
python scrape_to_json.py https://state1.example.gov \
    --output state1.json

# Apply same schema to Site 2 (similar structure)
python scrape_to_json.py https://state2.example.gov \
    --schema ./scraped_data/json/schema_analysis.json \
    --output state2.json

# Now both datasets have identical structure!
```

**When to reuse schemas:**

1. **Regular Updates**: Website that gets updated monthly/quarterly
   - Use the same schema each time
   - Data remains mergeable and comparable

2. **Multiple Similar Sites**: State agencies, regional sites, mirrors
   - Generate schema from first site
   - Apply to all others

3. **Version Tracking**: Monitor website changes over time
   - Keep baseline schema
   - See what changes in content structure

4. **Database Consistency**: Multiple data sources into one database
   - One schema for all sources
   - Simplified database design

**Schema file format:**

The schema file can be:
- The complete `schema_analysis.json` (recommended)
- Just the schema object itself

Example `schema_analysis.json`:
```json
{
  "content_type": "Medical Documentation",
  "entities": ["condition", "criteria", "symptoms"],
  "schema": {
    "condition_name": "string",
    "condition_code": "string",
    "body_system": "string",
    "criteria": "array",
    "notes": "string"
  },
  "indexes": ["condition_code", "body_system"],
  "notes": "Schema for medical disability criteria"
}
```

**See also:** `examples/schema_reuse_example.sh` for a complete demonstration.

## Performance Tips

1. **Rate Limiting**: Be respectful to servers
   ```bash
   --delay 2.0  # 2 seconds between requests
   ```

2. **Page Limits**: Start small, scale up
   ```bash
   --max-pages 50  # Test run
   --max-pages 1000  # Full crawl
   ```

3. **Depth Control**: Avoid infinite loops
   ```bash
   --max-depth 2  # For broad sites
   --max-depth 4  # For deep hierarchies
   ```

4. **Provider Selection**: Match task to AI
   - Gemini: Fast, cheap, good for large volumes
   - Claude: Accurate, best for complex structures
   - OpenAI: Balanced, good for mixed content

5. **Batch Processing**: Automatic progress saves every 5 pages

## Troubleshooting

### "403 Forbidden" Errors

Some sites block automated tools. The crawler uses realistic headers, but if blocked:
- Increase `--delay` to 2-3 seconds
- Reduce `--max-pages` for smaller batches
- Check site's robots.txt and terms of service

### AI Conversion Failures

If conversion fails:
- Check API key is set correctly
- Try a different provider
- Use `--conversion-delay 3.0` for slower rate
- Check the raw data in `scraped_data/json/scraped_data.json`

### Out of Memory

For very large sites:
- Reduce `--max-pages`
- Process in batches
- Use `--skip-conversion` and convert later

### Invalid JSON Output

If AI generates invalid JSON:
- Check `schema_analysis.json` for parsing errors
- Try a different AI provider (Claude is most reliable)
- Inspect failed URLs in the conversion output

## Example Use Cases

### 1. SSA Blue Book (Primary Example)

**Scenario**: Create a searchable database of disability criteria

```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --provider claude \
    --output ssa_bluebook.json
```

**Result**: JSON with impairment codes, body systems, criteria, all searchable and indexed

### 2. Medical Guidelines

**Scenario**: Archive medical treatment guidelines

```bash
python scrape_to_json.py https://guidelines.medical.org \
    --include "/guidelines/" \
    --max-depth 2 \
    --provider claude \
    --output medical_guidelines.json
```

### 3. Legal Code/Regulations

**Scenario**: Convert legal code to searchable database

```bash
python scrape_to_json.py https://laws.example.gov \
    --include "/title-" \
    --max-depth 4 \
    --provider claude \
    --output legal_code.json
```

### 4. Product Documentation

**Scenario**: Create offline product documentation

```bash
python scrape_to_json.py https://docs.product.com \
    --include "/docs/" \
    --exclude "/api-reference/" \
    --provider gemini \
    --output product_docs.json
```

## Comparison with Other Tools

| Feature | This Tool | wget -m | HTTrack |
|---------|-----------|---------|---------|
| Recursive crawling | ✅ | ✅ | ✅ |
| Offline storage | ✅ | ✅ | ✅ |
| JavaScript support | ✅ (Playwright) | ❌ | ⚠️ Limited |
| Structured JSON export | ✅ | ❌ | ❌ |
| AI-powered analysis | ✅ | ❌ | ❌ |
| Database-ready output | ✅ | ❌ | ❌ |
| Schema generation | ✅ | ❌ | ❌ |
| Content extraction | ✅ | ❌ | ⚠️ Basic |

## API Costs (Estimated)

For a typical 100-page site:

- **Gemini**: ~$0.10-0.50 (very affordable)
- **Claude**: ~$2-5 (higher quality)
- **OpenAI**: ~$1-3 (balanced)

Costs vary based on page size and complexity.

## License

Same as the main project.

## Contributing

Contributions welcome! Areas for improvement:
- Additional AI providers
- More database integration examples
- Specialized extractors for common site types
- Resume capability for AI conversion
- Parallel processing for faster conversion

## Support

For issues specific to data retrieval:
1. Check the generated README.md in output directory
2. Verify API keys are set correctly
3. Review `crawl_progress.json` for crawl issues
4. Check `schema_analysis.json` for schema problems

For general issues, see main README.md
