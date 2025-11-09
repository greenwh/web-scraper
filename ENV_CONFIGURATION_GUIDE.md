# .env Configuration Guide

## Overview

The web scraper now supports `.env` files for managing API keys and model configurations. This is the recommended way to configure your AI providers instead of using `export` commands.

## Benefits of Using .env Files

✅ **Centralized Configuration** - All API keys and models in one file
✅ **Easier to Manage** - Edit one file instead of multiple export commands
✅ **Persistent** - Configuration survives terminal restarts
✅ **Secure** - .env file is in .gitignore (won't be committed)
✅ **Model Customization** - Easily switch between different AI models
✅ **Cost Control** - Use cheaper models for testing, better models for production

## Setup (2 Steps)

### Step 1: Create Your .env File

```bash
# Copy the example file
cp .env.example .env

# Edit with your favorite editor
nano .env
# or
vim .env
# or
code .env
```

### Step 2: Fill In Your API Keys

```bash
# .env file contents
ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
ANTHROPIC_API_MODEL="claude-3-5-sonnet-20241022"

GOOGLE_API_KEY="your-actual-key-here"
GEMINI_API_MODEL="gemini-2.0-flash-exp"

OPENAI_API_KEY="sk-proj-your-actual-key-here"
OPENAI_API_MODEL="gpt-4-turbo-preview"

XAI_API_KEY="xai-your-actual-key-here"
XAI_API_MODEL="grok-beta"
```

**That's it!** No need for `export` commands anymore.

## Configuration Options

### API Keys (Required)

You only need API keys for the providers you plan to use:

| Variable | Provider | Get Key From |
|----------|----------|--------------|
| `ANTHROPIC_API_KEY` | Claude | https://console.anthropic.com/ |
| `GOOGLE_API_KEY` | Gemini | https://makersuite.google.com/app/apikey |
| `OPENAI_API_KEY` | OpenAI | https://platform.openai.com/api-keys |
| `XAI_API_KEY` | Grok | https://x.ai/ |

### Model Names (Optional)

Model names have defaults but can be customized:

#### Anthropic Claude Models

```bash
ANTHROPIC_API_MODEL="claude-3-5-sonnet-20241022"  # Default - balanced
# ANTHROPIC_API_MODEL="claude-3-5-haiku-20241022"   # Fast & cheap
# ANTHROPIC_API_MODEL="claude-3-opus-20240229"      # Most powerful
```

**Use cases:**
- **Haiku**: Fast testing, simple content, cost-effective
- **Sonnet**: General use, good balance of speed/accuracy (default)
- **Opus**: Complex medical/legal content, highest accuracy

#### Google Gemini Models

```bash
GEMINI_API_MODEL="gemini-2.0-flash-exp"  # Default - fast & free
# GEMINI_API_MODEL="gemini-1.5-pro"       # More capable
# GEMINI_API_MODEL="gemini-1.5-flash"     # Even faster
```

**Use cases:**
- **Flash**: Testing, large-scale crawling, budget-friendly
- **Pro**: Better accuracy, complex content

#### OpenAI Models

```bash
OPENAI_API_MODEL="gpt-4-turbo-preview"  # Default
# OPENAI_API_MODEL="gpt-4"               # Most capable
# OPENAI_API_MODEL="gpt-4o-mini"         # Cheaper option
# OPENAI_API_MODEL="gpt-3.5-turbo"       # Fastest & cheapest
```

**Use cases:**
- **GPT-4**: Best quality, complex content
- **GPT-4-Turbo**: Faster, similar quality (default)
- **GPT-4o-Mini**: Good balance of cost and quality
- **GPT-3.5-Turbo**: Quick tests, simple content

#### xAI Grok Models

```bash
XAI_API_MODEL="grok-beta"  # Default - current public version
```

## Usage Examples

### Before (Old Way - Still Works)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-proj-..."
python scrape_to_json.py https://example.com --provider claude
```

### After (New Way - Recommended)

```bash
# Just edit .env once, then run commands
python scrape_to_json.py https://example.com --provider claude
```

**No more export commands needed!**

## Model Selection Strategy

### For Testing / Development

Use faster, cheaper models:

```bash
# .env
ANTHROPIC_API_MODEL="claude-3-5-haiku-20241022"
GEMINI_API_MODEL="gemini-2.0-flash-exp"
OPENAI_API_MODEL="gpt-4o-mini"
```

### For Production / SSA Blue Book

Use more powerful models:

```bash
# .env
ANTHROPIC_API_MODEL="claude-3-5-sonnet-20241022"  # Best for medical
GEMINI_API_MODEL="gemini-1.5-pro"
OPENAI_API_MODEL="gpt-4-turbo-preview"
```

### For Budget-Conscious Usage

```bash
# .env
GEMINI_API_MODEL="gemini-2.0-flash-exp"  # Free tier available
```

## Real-World Examples

### Example 1: SSA Blue Book with Claude Sonnet

```bash
# .env
ANTHROPIC_API_KEY="sk-ant-actual-key"
ANTHROPIC_API_MODEL="claude-3-5-sonnet-20241022"

# Command
python crawl_adult_listings.py --provider claude
```

### Example 2: Testing with Multiple Providers

```bash
# .env - Set up all providers
ANTHROPIC_API_KEY="sk-ant-..."
ANTHROPIC_API_MODEL="claude-3-5-haiku-20241022"  # Cheap for testing

GOOGLE_API_KEY="..."
GEMINI_API_MODEL="gemini-2.0-flash-exp"  # Free tier

OPENAI_API_KEY="sk-proj-..."
OPENAI_API_MODEL="gpt-4o-mini"  # Cheaper option

# Test with each
python scrape_to_json.py https://example.com --provider claude --max-pages 5
python scrape_to_json.py https://example.com --provider gemini --max-pages 5
python scrape_to_json.py https://example.com --provider openai --max-pages 5
```

### Example 3: Salvage Data with Grok

```bash
# .env
XAI_API_KEY="xai-actual-key"
XAI_API_MODEL="grok-beta"

# Command
python salvage_scraped_data.py ./scraped_data/json/scraped_data.json --provider grok
```

## Checking Your Configuration

### Verify .env File Exists

```bash
ls -la .env
# Should show your .env file
# Should NOT be tracked by git (check with git status)
```

### Test API Keys

```bash
# Quick Python test
python3 << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv()

print("Checking API keys...")
print(f"ANTHROPIC_API_KEY: {'✓ Set' if os.getenv('ANTHROPIC_API_KEY') else '✗ Not set'}")
print(f"GOOGLE_API_KEY: {'✓ Set' if os.getenv('GOOGLE_API_KEY') else '✗ Not set'}")
print(f"OPENAI_API_KEY: {'✓ Set' if os.getenv('OPENAI_API_KEY') else '✗ Not set'}")
print(f"XAI_API_KEY: {'✓ Set' if os.getenv('XAI_API_KEY') else '✗ Not set'}")

print("\nChecking models...")
print(f"ANTHROPIC_API_MODEL: {os.getenv('ANTHROPIC_API_MODEL') or 'Using default'}")
print(f"GEMINI_API_MODEL: {os.getenv('GEMINI_API_MODEL') or 'Using default'}")
print(f"OPENAI_API_MODEL: {os.getenv('OPENAI_API_MODEL') or 'Using default'}")
print(f"XAI_API_MODEL: {os.getenv('XAI_API_MODEL') or 'Using default'}")
EOF
```

## Troubleshooting

### "Module not found: dotenv"

```bash
pip install python-dotenv
```

### ".env file not being read"

Make sure you're in the correct directory:

```bash
# Check current directory
pwd

# Should be in web-scraper directory
# .env file should be in same directory as scrape_to_json.py
ls -la | grep .env
```

### "API key still not found"

1. Check .env file exists: `ls -la .env`
2. Check .env file has correct format (no spaces around =)
3. Make sure quotes are included:
   ```bash
   # Correct
   ANTHROPIC_API_KEY="sk-ant-..."

   # Incorrect
   ANTHROPIC_API_KEY=sk-ant-...
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

### "Using wrong model"

Priority order for model selection:
1. **Command-line parameter** (if you pass model to script directly)
2. **Environment variable** (from .env file)
3. **Default** (hardcoded in ai_converter.py)

Check which model is being used:
```bash
# The script will print which model it's using
python scrape_to_json.py https://example.com --provider claude
# Look for: "Initialized AI converter with claude provider"
```

## Security Best Practices

### ✅ DO

- ✅ Keep .env file in .gitignore
- ✅ Use .env.example for documentation
- ✅ Set restrictive permissions: `chmod 600 .env`
- ✅ Create separate .env files for different projects
- ✅ Rotate API keys periodically

### ❌ DON'T

- ❌ Commit .env to git
- ❌ Share your .env file
- ❌ Use production keys for testing
- ❌ Store .env in cloud storage
- ❌ Include .env in backups shared with others

## Migrating from Export Commands

### Old Setup

```bash
# ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

### New Setup

```bash
# .env file in project directory
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="..."
```

**Advantages:**
- Project-specific configuration
- Easier to manage multiple projects
- Can use different keys/models per project
- No pollution of global environment

## Default Models Reference

If you don't specify a model, these defaults are used:

| Provider | Default Model | Cost Tier |
|----------|--------------|-----------|
| Claude | `claude-3-5-sonnet-20241022` | Mid |
| Gemini | `gemini-2.0-flash-exp` | Free/Low |
| OpenAI | `gpt-4-turbo-preview` | Mid-High |
| Grok | `grok-beta` | Mid |

## Quick Start Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Add at least one API key
- [ ] (Optional) Customize model names
- [ ] Verify .env is in .gitignore
- [ ] Test with a simple command
- [ ] Delete old export commands from shell profile

## Summary

**Old way:**
```bash
export ANTHROPIC_API_KEY="..."
export ANTHROPIC_API_MODEL="..."
python scrape_to_json.py https://example.com --provider claude
```

**New way:**
```bash
# Edit .env once
ANTHROPIC_API_KEY="..."
ANTHROPIC_API_MODEL="..."

# Then just run
python scrape_to_json.py https://example.com --provider claude
```

**Much cleaner and easier to manage!** 🎉

## Next Steps

1. Create your `.env` file from the example
2. Add your API keys
3. (Optional) Customize model names for your use case
4. Run your scraping commands
5. Check `SSA_BLUEBOOK_DATA_GUIDE.md` for Blue Book specific instructions

For more information:
- **QUICKSTART.md** - General usage
- **DATA_RETRIEVAL_README.md** - Complete feature documentation
- **SALVAGE_GUIDE.md** - Data recovery instructions
