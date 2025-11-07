# Data Salvage Guide

This guide will help you find and convert your SSA Blue Book scraped data to structured JSON.

## What Happened?

You attempted to scrape the SSA Blue Book but ran into API issues. This guide will help you:
1. 🔍 Find your scraped data (if it exists)
2. 🔄 Convert it to structured JSON using working AI providers
3. 📊 Get the schema and data you need

## ✨ New Feature: Grok Support Added

We've added support for xAI's Grok AI provider. You now have 4 AI options:
- **Gemini** (Google) - Fast and cost-effective
- **Claude** (Anthropic) - Best for complex medical/legal content
- **OpenAI** - Balanced performance
- **Grok** (xAI) - NEW! Alternative option

## 📍 Step 1: Find Your Scraped Data

### Quick Check (Current Directory)

```bash
# Check if scraped_data exists here
ls -la scraped_data/

# If it exists, check the contents
ls -la scraped_data/json/
```

### Automated Search

We've created a script to search your entire system:

```bash
./find_scraped_data.sh
```

This will search for:
- `scraped_data` directories
- Files with "ssa", "bluebook", or "blue_book" in the name
- Large JSON files that might be scraped data

### Common Locations

Check these locations manually:
- `./scraped_data/json/scraped_data.json` (default location)
- `~/scraped_data/json/scraped_data.json`
- `~/Downloads/scraped_data.json`
- `~/Documents/web-scraper/scraped_data/`

## 📦 Step 2: What Data Do You Have?

### If You Have `scraped_data.json`

✅ **Good news!** The crawler worked and saved raw data. You just need to convert it.

Check what's in it:
```bash
# See how many pages
cat scraped_data/json/scraped_data.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Pages: {len(data)}')"

# See first page info
cat scraped_data/json/scraped_data.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data[0], indent=2))" | head -50
```

### If You Have HTML Files

Check `scraped_data/html/` directory:
```bash
ls -la scraped_data/html/ | head -20
```

If HTML exists but no JSON, the crawler saved pages but didn't extract structured data.

### If You Have Nothing

You'll need to run the scraper again. Skip to **Step 5**.

## 🔄 Step 3: Salvage Your Data

We've created a special salvage script to convert your existing scraped data.

### Basic Salvage (Using Gemini)

```bash
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json
```

### Salvage with Different AI Providers

**Using Claude (Best for SSA Blue Book):**
```bash
export ANTHROPIC_API_KEY="your-api-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider claude
```

**Using OpenAI:**
```bash
export OPENAI_API_KEY="your-api-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider openai
```

**Using Grok (NEW):**
```bash
export XAI_API_KEY="your-api-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider grok
```

**Using Gemini:**
```bash
export GOOGLE_API_KEY="your-api-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider gemini
```

### Salvage with Custom Output

```bash
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json \
    --provider claude \
    --output ssa_bluebook_final.json \
    --conversion-delay 2.0
```

## 🎯 Step 4: What You'll Get

After salvaging, you'll have:

```
.
├── ssa_bluebook_final.json              # ⭐ Your structured data
├── ssa_bluebook_final_schema.json       # 📋 Schema for database
└── scraped_data/
    ├── html/                            # Raw HTML files
    └── json/
        └── scraped_data.json            # Raw extracted data
```

### The Schema

The schema will contain:
- Field names and types
- Entity definitions
- Recommended database indexes
- Notes about the data structure

**Example for SSA Blue Book:**
```json
{
  "content_type": "Medical Disability Criteria",
  "entities": ["impairment", "body_system", "criteria"],
  "schema": {
    "impairment_code": "string",
    "impairment_name": "string",
    "body_system": "string",
    "criteria": "array",
    "severity_levels": "array"
  },
  "indexes": ["impairment_code", "body_system"],
  "notes": "SSA Adult Disability Listings"
}
```

### The Data

Each entry will follow the schema. **Example:**
```json
{
  "impairment_code": "1.00",
  "impairment_name": "Musculoskeletal Disorders",
  "body_system": "Musculoskeletal System",
  "criteria": [...],
  "_metadata": {
    "source_url": "https://www.ssa.gov/...",
    "title": "1.00 Musculoskeletal Disorders - Adult Listings",
    "scraped_at": 1699294800.0
  }
}
```

## 🔧 Step 5: If You Need to Re-Scrape

If you have no data or the data is incomplete:

### Set Up API Key

Choose ONE provider and set its API key:

```bash
# Gemini (recommended - free tier available)
export GOOGLE_API_KEY="your-api-key"

# Claude (best for complex medical content)
export ANTHROPIC_API_KEY="your-api-key"

# OpenAI
export OPENAI_API_KEY="your-api-key"

# Grok (NEW)
export XAI_API_KEY="your-api-key"
```

### Run the Scraper

**Full SSA Blue Book (Adults):**
```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --provider gemini \
    --output ssa_bluebook.json
```

**With Claude (Best Quality):**
```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 \
    --max-pages 200 \
    --provider claude \
    --conversion-delay 2.0 \
    --output ssa_bluebook.json
```

**Test with Small Sample First:**
```bash
python scrape_to_json.py \
    https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 1 \
    --max-pages 5 \
    --provider gemini \
    --output test_bluebook.json
```

## 🆘 Troubleshooting

### "File not found" Error

```bash
# Find where your data is
./find_scraped_data.sh

# Or search manually
find ~ -name "scraped_data.json" 2>/dev/null
```

### API Key Errors

Make sure your API key is set:
```bash
# Check if set
echo $GOOGLE_API_KEY
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
echo $XAI_API_KEY

# If empty, set it
export GOOGLE_API_KEY="your-actual-key-here"
```

### "Module not found" Errors

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt
```

### Conversion Fails

If one AI provider fails, try another:

```bash
# If Gemini fails, try Claude
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider claude

# If Claude fails, try OpenAI
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider openai

# Try the new Grok provider
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider grok
```

### Rate Limiting

If you hit rate limits:
```bash
# Increase delay between API calls
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json \
    --conversion-delay 5.0 \
    --batch-size 3
```

## 📋 Quick Reference

### Find Data
```bash
./find_scraped_data.sh
```

### Salvage Data (Gemini)
```bash
export GOOGLE_API_KEY="your-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json
```

### Salvage Data (Claude - Best for Medical)
```bash
export ANTHROPIC_API_KEY="your-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider claude
```

### Salvage Data (Grok - NEW)
```bash
export XAI_API_KEY="your-key"
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider grok
```

### Re-Scrape from Scratch
```bash
export GOOGLE_API_KEY="your-key"
python scrape_to_json.py https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm \
    --max-depth 3 --max-pages 200 --output ssa_bluebook.json
```

## 🎯 What You Need

Based on your request for "adult listings" from the SSA Blue Book:

**Target URL:** https://www.ssa.gov/disability/professionals/bluebook/AdultListings.htm

**What You'll Get:**
- All adult impairment listings (1.00 - 14.00+)
- Body systems: Musculoskeletal, Special Senses, Respiratory, Cardiovascular, etc.
- Detailed medical criteria for each impairment
- Severity levels and functional requirements
- All in searchable, database-ready JSON format

**Recommended Settings:**
- `--max-depth 3` (captures all linked pages)
- `--max-pages 200` (enough for complete Blue Book)
- `--provider claude` (best for complex medical content)
- `--conversion-delay 2.0` (polite rate limiting)

## 📊 Expected Results

For the SSA Blue Book, you should get:
- **~50-150 pages** of content (depending on how deep it crawls)
- **Body systems:** 14+ major categories
- **Impairments:** 100+ specific conditions
- **Structured fields:** Codes, names, criteria, notes
- **Database-ready:** JSON with schema and indexes

## 🔍 Verify Your Data

After conversion, check what you got:

```bash
# Count entries
cat ssa_bluebook_final.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Total entries: {len(data)}')"

# See a sample entry
cat ssa_bluebook_final.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(data[0], indent=2))"

# Check the schema
cat ssa_bluebook_final_schema.json | python3 -m json.tool
```

## ✅ Success Checklist

- [ ] Found or scraped raw data (scraped_data.json)
- [ ] Set up API key for chosen provider
- [ ] Ran salvage script successfully
- [ ] Got structured JSON output
- [ ] Got schema file
- [ ] Verified data contains adult listings
- [ ] Data is ready for database import

---

## Need Help?

If you're stuck:
1. Run `./find_scraped_data.sh` to locate your data
2. Check the error messages - they usually tell you what's missing
3. Try a different AI provider if one fails
4. Start with a small test (5 pages) before full scrape

Good luck! 🎉
