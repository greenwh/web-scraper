# Git Sync Guide - Pulling Remote Changes to Your Local Machine

This guide will help you sync the changes from the remote repository to your local machine and test them.

## 📍 Step 1: Navigate to Your Local Repository

Open your terminal/command prompt and navigate to where you have the web-scraper repository on your local machine.

```bash
# Example - adjust the path to match your local setup
cd /path/to/your/web-scraper

# On Windows, it might look like:
# cd C:\Users\YourName\Projects\web-scraper

# On Mac/Linux, it might look like:
# cd ~/Projects/web-scraper
```

**Verify you're in the right place:**
```bash
# This should show your repository name
pwd

# This should show git information
git status
```

## 📥 Step 2: Fetch All Remote Changes

First, fetch all the changes from GitHub without modifying your local files:

```bash
git fetch origin
```

**What this does:** Downloads all the new branches and commits from GitHub, but doesn't change your local files yet.

## 🔍 Step 3: Check What Branches Are Available

See all the branches, including the new one from the remote:

```bash
# See all remote branches
git branch -r

# You should see something like:
#   origin/main
#   origin/claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
```

## 🌿 Step 4: Switch to the New Branch

Switch to the branch that contains the new features:

```bash
git checkout claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
```

**What this does:** Creates a local copy of the remote branch and switches to it.

**Alternative (if the above doesn't work):**
```bash
git checkout -b claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc origin/claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
```

**Verify you're on the right branch:**
```bash
git branch
# The current branch will have an asterisk (*) next to it
```

## 📦 Step 5: Install Dependencies

Now that you have the new code, install any new dependencies:

### If you already have a virtual environment:

```bash
# Activate your existing virtual environment
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate  # On Windows

# Update dependencies
pip install -r requirements.txt
```

### If you DON'T have a virtual environment yet:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate  # On Windows

# Install all dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Set up API Key (if not already done):

```bash
# Set at least one API key for testing
export GOOGLE_API_KEY="your-gemini-api-key"

# On Windows (Command Prompt):
# set GOOGLE_API_KEY=your-gemini-api-key

# On Windows (PowerShell):
# $env:GOOGLE_API_KEY="your-gemini-api-key"
```

## 🧪 Step 6: Test the New Features

### Quick Test - Run the test suite:

```bash
python test_modules.py
```

This tests basic functionality without making API calls.

### Test Schema Reuse Feature:

```bash
python test_schema_reuse.py
```

This will create an example schema and show usage examples.

### Test Interactive Mode (original feature):

```bash
python main.py
```

Follow the prompts to test interactive browsing.

### Test Data Retrieval Mode (new feature):

**Simple test with example.com:**
```bash
python scrape_to_json.py http://example.com \
    --max-depth 0 \
    --max-pages 1 \
    --output test_output.json
```

**Test schema reuse:**
```bash
# First run (generates schema)
python scrape_to_json.py http://example.com \
    --max-depth 0 \
    --max-pages 1 \
    --output test1.json

# Second run (reuses schema)
python scrape_to_json.py http://example.com \
    --max-depth 0 \
    --max-pages 1 \
    --schema ./scraped_data/json/schema_analysis.json \
    --output test2.json
```

### Check the output:

```bash
# See what files were created
ls -la scraped_data/

# View the schema
cat scraped_data/json/schema_analysis.json

# View structured data
cat test_output.json
```

## ✅ Step 7: Review the New Features

Check out the documentation for the new features:

```bash
# Quick start guide
cat QUICKSTART.md

# Comprehensive data retrieval guide
cat DATA_RETRIEVAL_README.md

# Technical details
cat CLAUDE.md
```

**New Features Added:**
1. ✅ Recursive website crawling (like wget -m)
2. ✅ AI-powered JSON conversion (Gemini, Claude, OpenAI)
3. ✅ Automatic schema generation
4. ✅ **Schema reuse for consistent parsing** ⭐ NEW
5. ✅ Database-ready JSON export
6. ✅ Progress tracking and resumption

## 🔀 Step 8: Merge to Main Branch (After Testing)

Once you've tested everything and you're satisfied:

### Option A: Merge Locally

```bash
# Switch to main branch
git checkout main

# Pull latest main (in case there were other changes)
git pull origin main

# Merge the feature branch
git merge claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc

# Push the updated main to GitHub
git push origin main
```

### Option B: Create a Pull Request on GitHub (Recommended)

1. Go to your GitHub repository in a web browser
2. You should see a banner saying "Compare & pull request"
3. Click it and review the changes
4. Add a description if needed
5. Click "Create pull request"
6. Review and click "Merge pull request"
7. Then pull the updated main to your local machine:

```bash
git checkout main
git pull origin main
```

### Clean Up the Feature Branch (Optional)

After merging, you can delete the feature branch:

```bash
# Delete local branch
git branch -d claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc

# Delete remote branch
git push origin --delete claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
```

## 🤖 Using Claude Code for This Process

If you want Claude Code to handle this entire process for you, use this prompt:

```
I have a remote branch called "claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc"
in my web-scraper repository that contains new features.

Please:
1. Fetch the latest changes from the remote repository
2. Check out the feature branch
3. Verify the dependencies are installed
4. Run the test suite (test_modules.py and test_schema_reuse.py)
5. Show me a summary of what changed
6. If tests pass, help me merge this branch to main

Repository location: /path/to/your/web-scraper
```

## 📋 Quick Reference Commands

```bash
# Get to your repository
cd /path/to/your/web-scraper

# Fetch and checkout the branch
git fetch origin
git checkout claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Test
python test_modules.py
python test_schema_reuse.py

# Merge to main (after testing)
git checkout main
git merge claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
git push origin main
```

## 🆘 Troubleshooting

### "Branch not found" error
```bash
# Make sure you fetched first
git fetch origin

# Try checking out with -b flag
git checkout -b claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc origin/claude/website-scrape-json-export-011CUrRQpDTaS3raDzYZixuc
```

### "Merge conflict" error
```bash
# See which files have conflicts
git status

# You'll need to edit the conflicting files manually
# Look for markers like <<<<<<< HEAD

# After fixing conflicts:
git add .
git commit -m "Resolved merge conflicts"
```

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
playwright install chromium
```

### Tests failing
```bash
# Check if API key is set
echo $GOOGLE_API_KEY  # Should show your key

# If not set:
export GOOGLE_API_KEY="your-key"

# Try running tests again
python test_modules.py
```

## 📚 Documentation Files

After syncing, check out these files for detailed information:

- **QUICKSTART.md** - 5-minute setup guide
- **DATA_RETRIEVAL_README.md** - Complete feature documentation
- **CLAUDE.md** - Technical architecture details
- **README.md** - Project overview
- **examples/schema_reuse_example.sh** - Schema reuse demonstration

## 🎉 You're Done!

After following these steps, you'll have:
- ✅ The latest code on your local machine
- ✅ All dependencies installed
- ✅ Tests verified
- ✅ Features merged to main (if desired)

If you run into any issues, refer to the troubleshooting section above or check the documentation files.

## Summary of Changes in This Branch

**New Features:**
1. Recursive website crawler (`crawler.py`)
2. AI-powered JSON converter (`ai_converter.py`)
3. Main integration script (`scrape_to_json.py`)
4. Schema reuse capability (`--schema` parameter)
5. Multi-AI provider support (Gemini, Claude, OpenAI)

**New Files:**
- `crawler.py` - Website crawling engine
- `ai_converter.py` - AI conversion with multi-provider support
- `scrape_to_json.py` - Main data retrieval script
- `test_modules.py` - Unit tests
- `test_schema_reuse.py` - Schema reuse tests
- `examples/ssa_bluebook_config.sh` - SSA Blue Book example
- `examples/schema_reuse_example.sh` - Schema reuse demo
- `example_schema.json` - Example schema file
- `DATA_RETRIEVAL_README.md` - Comprehensive guide
- `QUICKSTART.md` - Quick start guide

**Updated Files:**
- `README.md` - Added feature overview
- `CLAUDE.md` - Updated architecture documentation
- `requirements.txt` - Added anthropic and openai

**Commits:**
- Initial feature implementation (website data retrieval & JSON export)
- Schema reuse capability addition
