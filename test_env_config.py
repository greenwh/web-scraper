#!/usr/bin/env python3
"""
Test script for .env configuration

Verifies that API keys and models are being read correctly from .env file.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("="*70)
print(".ENV CONFIGURATION TEST")
print("="*70)
print()

# Check if .env file exists
from pathlib import Path
env_file = Path(".env")
if env_file.exists():
    print("✓ .env file found")
else:
    print("✗ .env file not found")
    print("  Create one with: cp .env.example .env")
    print()

print()
print("API Keys Configuration:")
print("-"*70)

# Check API keys
providers = {
    "Anthropic Claude": "ANTHROPIC_API_KEY",
    "Google Gemini": "GOOGLE_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
    "xAI Grok": "XAI_API_KEY"
}

configured_providers = []
for name, var in providers.items():
    value = os.getenv(var)
    if value:
        # Show first 10 and last 4 characters for security
        masked = value[:10] + "..." + value[-4:] if len(value) > 14 else value[:6] + "..."
        print(f"✓ {name:20} {var:25} {masked}")
        configured_providers.append(name.split()[0].lower())
    else:
        print(f"✗ {name:20} {var:25} Not set")

print()
print("Model Configuration:")
print("-"*70)

# Check model configurations
models = {
    "Anthropic Claude": ("ANTHROPIC_API_MODEL", "claude-3-5-sonnet-20241022"),
    "Google Gemini": ("GEMINI_API_MODEL", "gemini-2.0-flash-exp"),
    "OpenAI": ("OPENAI_API_MODEL", "gpt-4-turbo-preview"),
    "xAI Grok": ("XAI_API_MODEL", "grok-beta")
}

for name, (var, default) in models.items():
    value = os.getenv(var)
    if value:
        print(f"✓ {name:20} {var:25} {value}")
    else:
        print(f"○ {name:20} {var:25} Using default: {default}")

print()
print("="*70)
print("SUMMARY")
print("="*70)

if configured_providers:
    print(f"\n✓ {len(configured_providers)} provider(s) configured:")
    for provider in configured_providers:
        print(f"  - {provider}")
    print("\nYou can use these providers:")
    for provider in configured_providers:
        print(f"  python scrape_to_json.py https://example.com --provider {provider}")
else:
    print("\n✗ No providers configured")
    print("\nTo configure providers:")
    print("  1. Copy the example: cp .env.example .env")
    print("  2. Edit the file: nano .env")
    print("  3. Add at least one API key")
    print("  4. Run this test again")

print()

# Test importing AI converter
print("Testing AI Converter Module:")
print("-"*70)
try:
    from ai_converter import AIDataConverter
    print("✓ ai_converter module imported successfully")

    # Test each configured provider
    for provider in configured_providers:
        try:
            converter = AIDataConverter(provider=provider)
            print(f"✓ {provider.capitalize()} provider initialized successfully")
        except Exception as e:
            print(f"✗ {provider.capitalize()} provider failed: {e}")

except Exception as e:
    print(f"✗ Failed to import ai_converter: {e}")

print()
print("="*70)
print("TEST COMPLETE")
print("="*70)
print()

if not configured_providers:
    print("⚠️  No providers configured. Please set up your .env file.")
    print("   See ENV_CONFIGURATION_GUIDE.md for details.")
else:
    print("✓ Configuration looks good!")
    print("  Ready to start scraping!")

print()
