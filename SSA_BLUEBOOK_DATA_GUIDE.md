# SSA Blue Book Data - Complete Guide

## 📊 What You Have

**Location:** `ssa_bluebook_data/json/scraped_data.json`

**Current Data:**
- ✅ **41 pages** total
- ✅ **14 pages with tables**
- ⚠️ **Only 2 adult listing pages** (index + consultative exam guide)
- 📝 **17 childhood listings** (100.00, 101.00, 103.00, 105.00 series)
- 📄 **22 general information pages**

**The Issue:**
The original crawl found links to all 14 adult impairment listings (1.00-14.00) but didn't follow them. The links exist in the data but the actual listing pages weren't scraped.

## 🎯 What You Need

You want the **complete adult listings** which include:

1. **1.00** - Musculoskeletal Disorders
2. **2.00** - Special Senses and Speech
3. **3.00** - Respiratory Disorders
4. **4.00** - Cardiovascular System
5. **5.00** - Digestive System
6. **6.00** - Genitourinary Disorders
7. **7.00** - Hematological Disorders
8. **8.00** - Skin Disorders
9. **9.00** - Endocrine Disorders
10. **10.00** - Congenital Disorders (Multiple Body Systems)
11. **11.00** - Neurological Disorders
12. **12.00** - Mental Disorders
13. **13.00** - Cancer (Malignant Neoplastic Diseases)
14. **14.00** - Immune System Disorders

## 🚀 Solution: Get Complete Adult Listings

### Option 1: Run the Targeted Crawler (Recommended)

I've created a script that specifically fetches all 14 adult listing pages:

```bash
# Set your API key (choose one)
export GOOGLE_API_KEY="your-key"        # Gemini (recommended)
export ANTHROPIC_API_KEY="your-key"     # Claude (best for medical)
export OPENAI_API_KEY="your-key"        # OpenAI

# Run the targeted crawler
python crawl_adult_listings.py --provider claude

# Output will be in: ./ssa_adult_listings/
```

**What this does:**
- Fetches all 14 adult listing pages directly
- Extracts text, headings, and tables
- Converts to structured JSON with AI
- Generates proper Blue Book schema
- Creates database-ready output

**Output files:**
```
ssa_adult_listings/
├── ssa_bluebook_adult_complete.json    # ⭐ Complete adult listings
├── json/
│   ├── scraped_data.json              # Raw crawled data
│   └── schema_analysis.json           # Generated schema
└── html/                              # Raw HTML files
```

### Option 2: Use Existing Data (Partial)

If you want to work with what's already scraped:

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Salvage with custom Blue Book schema
python salvage_scraped_data.py \
    ./ssa_bluebook_data/json/scraped_data.json \
    --schema ./bluebook_schema.json \
    --provider claude \
    --output ssa_existing_data.json
```

**What you'll get:**
- Structured JSON of the 41 pages that were scraped
- Mostly childhood listings and general info
- Some adult-related pages
- NOT the complete adult impairment listings

### Option 3: Re-Crawl with Better Settings

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Re-crawl with more aggressive settings
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 2 \
    --max-pages 50 \
    --delay 2.0 \
    --provider claude \
    --include "/Adult.htm" \
    --output ssa_bluebook_recrawl.json
```

## 📋 Recommended Approach

**For Complete Adult Listings:** Use Option 1 (Targeted Crawler)

```bash
# 1. Set API key
export ANTHROPIC_API_KEY="your-api-key"  # Claude recommended for medical content

# 2. Run targeted crawler
python crawl_adult_listings.py --provider claude

# 3. Wait for completion (will take ~5-10 minutes)
#    - Fetches 14 pages
#    - Delay of 2 seconds between requests
#    - AI conversion with Claude

# 4. Check output
cat ssa_adult_listings/ssa_bluebook_adult_complete.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Total listings: {len(data)}')"
```

## 📊 Expected Final Output

After running the targeted crawler, you'll have:

**ssa_bluebook_adult_complete.json:**
```json
[
  {
    "listing_number": "1.00",
    "listing_title": "Musculoskeletal Disorders",
    "body_system": "Musculoskeletal System",
    "url": "https://www.ssa.gov/disability/professionals/bluebook/1.00-Musculoskeletal-Adult.htm",
    "main_content": "...",
    "criteria": [...],
    "tables": [...],
    "headings": [...],
    "_metadata": {
      "source_url": "...",
      "title": "...",
      "scraped_at": 1699294800.0
    }
  },
  {
    "listing_number": "2.00",
    "listing_title": "Special Senses and Speech",
    ...
  }
  ...
]
```

**bluebook_schema.json:**
```json
{
  "content_type": "SSA Disability Blue Book - Medical Impairment Listings",
  "entities": ["impairment_listing", "body_system", "criteria"],
  "schema": {
    "listing_number": "string",
    "listing_title": "string",
    "body_system": "string",
    "criteria": "array of objects",
    "tables": "array of arrays"
  },
  "indexes": ["listing_number", "body_system"]
}
```

## 🔧 AI Provider Recommendations

**For SSA Blue Book specifically:**

1. **Claude (Anthropic)** - **BEST CHOICE** ⭐
   - Excellent at medical/legal content
   - Accurate structure extraction
   - Good with tables and criteria
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   python crawl_adult_listings.py --provider claude
   ```

2. **Gemini (Google)** - Good Budget Option
   - Fast and cheap
   - Decent accuracy
   - Good for testing
   ```bash
   export GOOGLE_API_KEY="your-key"
   python crawl_adult_listings.py --provider gemini
   ```

3. **OpenAI (GPT)** - Balanced
   - Good accuracy
   - Mid-range cost
   ```bash
   export OPENAI_API_KEY="your-key"
   python crawl_adult_listings.py --provider openai
   ```

## 💾 Loading into Database

Once you have the JSON, load it into your database:

### MongoDB
```javascript
const data = require('./ssa_adult_listings/ssa_bluebook_adult_complete.json');
const { MongoClient } = require('mongodb');

const client = await MongoClient.connect('mongodb://localhost:27017');
const db = client.db('ssa');
const collection = db.collection('adult_listings');

await collection.insertMany(data);

// Create indexes
await collection.createIndex({ listing_number: 1 });
await collection.createIndex({ body_system: 1 });
await collection.createIndex({ listing_title: 'text' });

// Search example
const results = await collection.find({
  body_system: 'Musculoskeletal System'
}).toArray();
```

### PostgreSQL with JSONB
```sql
CREATE TABLE ssa_adult_listings (
    id SERIAL PRIMARY KEY,
    listing_number VARCHAR(10),
    body_system VARCHAR(100),
    data JSONB NOT NULL
);

-- Load data (use your preferred method)
-- Then query
SELECT * FROM ssa_adult_listings
WHERE data->>'body_system' = 'Cardiovascular System';

-- Full-text search
SELECT * FROM ssa_adult_listings
WHERE data->>'main_content' ILIKE '%heart failure%';
```

### SQLite with FTS
```python
import sqlite3
import json

conn = sqlite3.connect('ssa_bluebook.db')
cursor = conn.cursor()

# Create FTS table
cursor.execute('''
    CREATE VIRTUAL TABLE adult_listings USING fts5(
        listing_number,
        listing_title,
        body_system,
        main_content,
        criteria
    )
''')

# Load data
with open('ssa_adult_listings/ssa_bluebook_adult_complete.json', 'r') as f:
    data = json.load(f)
    for item in data:
        cursor.execute('''
            INSERT INTO adult_listings VALUES (?, ?, ?, ?, ?)
        ''', (
            item.get('listing_number'),
            item.get('listing_title'),
            item.get('body_system'),
            item.get('main_content'),
            json.dumps(item.get('criteria', []))
        ))

conn.commit()

# Search
results = cursor.execute('''
    SELECT * FROM adult_listings WHERE adult_listings MATCH 'diabetes'
''').fetchall()
```

## ⚠️ Important Notes

1. **Existing Data (ssa_bluebook_data):**
   - Has 41 pages but mostly childhood listings
   - Missing the 14 adult impairment listing pages
   - Can be salvaged but won't have complete adult info

2. **Complete Adult Data:**
   - Use `crawl_adult_listings.py` to get all 14 listings
   - This is what you need for adult disability criteria
   - Will create new directory: `ssa_adult_listings/`

3. **Both Combined:**
   - You can salvage existing data AND run targeted crawler
   - Combine both datasets if you want everything
   - Or just use targeted crawler for clean adult-only data

## 🧪 Quick Test

Test the targeted crawler with one page first:

```python
# Quick test script
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def test_fetch():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url = "https://www.ssa.gov/disability/professionals/bluebook/1.00-Musculoskeletal-Adult.htm"
        await page.goto(url, timeout=60000)

        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        title = soup.find('title').get_text()
        tables = len(soup.find_all('table'))

        print(f"Title: {title}")
        print(f"Tables found: {tables}")

        await browser.close()

asyncio.run(test_fetch())
```

## 📞 Need Help?

1. **Can't run crawler?**
   - Check API key is set: `echo $ANTHROPIC_API_KEY`
   - Check modules installed: `pip install -r requirements.txt`
   - Check Playwright: `playwright install chromium`

2. **Conversion fails?**
   - Try different AI provider
   - Check API key is valid
   - Increase delays if rate limited

3. **Want both adult and childhood?**
   - Run targeted crawler for adults
   - Salvage existing data for childhood
   - Combine JSON files manually or with script

## 🎯 Summary

**To get complete SSA Blue Book adult listings:**

```bash
# Quick version
export ANTHROPIC_API_KEY="your-key"
python crawl_adult_listings.py --provider claude

# You'll get:
# ssa_adult_listings/ssa_bluebook_adult_complete.json
# - All 14 adult impairment listings
# - Structured and database-ready
# - With proper schema
```

That's it! 🎉
