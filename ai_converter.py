"""
AI-Powered JSON Converter
Converts scraped website data into structured JSON using AI providers
Supports: Claude (Anthropic), Gemini (Google), OpenAI, and Grok (xAI)
"""

import os
import json
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AIProvider(ABC):
    """Base class for AI providers."""

    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        """Generate a response from the AI provider."""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        import google.generativeai as genai

        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        # Use model from parameter, env var, or default
        model_name = model or os.environ.get("GEMINI_API_MODEL") or "gemini-2.0-flash-exp"

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name

    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error with Gemini API: {e}")
            return None


class ClaudeProvider(AIProvider):
    """Anthropic Claude AI provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        # Use model from parameter, env var, or default
        self.model = model or os.environ.get("ANTHROPIC_API_MODEL") or "claude-3-5-sonnet-20241022"

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error with Claude API: {e}")
            return None


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Use model from parameter, env var, or default
        self.model = model or os.environ.get("OPENAI_API_MODEL") or "gpt-4-turbo-preview"

        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return None


class GrokProvider(AIProvider):
    """xAI Grok provider."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.environ.get("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY environment variable not set")

        # Use model from parameter, env var, or default
        self.model = model or os.environ.get("XAI_API_MODEL") or "grok-beta"

        try:
            import openai
            # Grok uses OpenAI SDK with custom base URL
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate_response(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error with Grok API: {e}")
            return None


class AIDataConverter:
    """
    Converts scraped website data into structured JSON using AI.
    """

    def __init__(self, provider: str = "gemini", **provider_kwargs):
        """
        Initialize the converter with an AI provider.

        Args:
            provider: AI provider name ('gemini', 'claude', 'openai', or 'grok')
            **provider_kwargs: Additional arguments for the provider
        """
        self.provider_name = provider.lower()

        if self.provider_name == "gemini":
            self.provider = GeminiProvider(**provider_kwargs)
        elif self.provider_name == "claude":
            self.provider = ClaudeProvider(**provider_kwargs)
        elif self.provider_name == "openai":
            self.provider = OpenAIProvider(**provider_kwargs)
        elif self.provider_name == "grok":
            self.provider = GrokProvider(**provider_kwargs)
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'gemini', 'claude', 'openai', or 'grok'")

        print(f"Initialized AI converter with {self.provider_name} provider")

    def analyze_data_structure(self, scraped_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze the scraped data to determine the optimal structure.

        Args:
            scraped_data: List of scraped page data

        Returns:
            Analysis results including recommended schema
        """
        print("Analyzing data structure...")

        # Sample a few pages for analysis
        sample_size = min(5, len(scraped_data))
        sample_pages = scraped_data[:sample_size]

        # Create analysis prompt
        prompt = f"""Analyze the following website data and determine the optimal JSON schema for storing it in a database.

The data comes from {len(scraped_data)} pages. Here are {sample_size} sample pages:

"""
        for i, page in enumerate(sample_pages, 1):
            prompt += f"\n--- Page {i} ---\n"
            prompt += f"URL: {page['url']}\n"
            prompt += f"Title: {page['title']}\n"
            prompt += f"Headings: {json.dumps(page['headings'][:5], indent=2)}\n"
            if page.get('tables'):
                prompt += f"Has {len(page['tables'])} table(s)\n"
            prompt += f"Content sample (first 500 chars): {page['text_content'][:500]}...\n"

        prompt += """

Based on this data, provide:
1. A description of the content type and structure
2. Key entities and relationships
3. A recommended JSON schema with field names, types, and descriptions
4. Suggested database indexes for searchability

Format your response as a JSON object with these keys:
- content_type: string describing the type of content
- entities: array of entity types found
- schema: detailed JSON schema object
- indexes: array of suggested index fields
- notes: additional observations

Return ONLY the JSON object, no other text.
"""

        response = self.provider.generate_response(prompt, max_tokens=4000)

        if not response:
            return {
                "content_type": "unknown",
                "entities": [],
                "schema": {},
                "indexes": [],
                "notes": "Analysis failed"
            }

        try:
            # Extract JSON from response (handle markdown code blocks)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]

            analysis = json.loads(response.strip())
            return analysis
        except json.JSONDecodeError as e:
            print(f"Failed to parse analysis JSON: {e}")
            print(f"Response was: {response[:500]}")
            return {
                "content_type": "unknown",
                "entities": [],
                "schema": {},
                "indexes": [],
                "notes": f"Failed to parse analysis: {str(e)}"
            }

    def convert_page_to_structured_data(
        self,
        page_data: Dict,
        schema: Dict,
        context: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Convert a single page to structured data based on the schema.

        Args:
            page_data: Scraped page data
            schema: Target JSON schema
            context: Additional context about the data

        Returns:
            Structured data following the schema
        """
        # Create conversion prompt
        prompt = f"""Convert the following webpage content into structured JSON data according to the provided schema.

TARGET SCHEMA:
{json.dumps(schema, indent=2)}

WEBPAGE DATA:
URL: {page_data['url']}
Title: {page_data['title']}

Headings:
{json.dumps(page_data['headings'], indent=2)}

"""

        if page_data.get('tables'):
            prompt += f"\nTables:\n{json.dumps(page_data['tables'], indent=2)}\n"

        prompt += f"""
Text Content:
{page_data['text_content'][:8000]}

"""

        if context:
            prompt += f"\nADDITIONAL CONTEXT:\n{context}\n"

        prompt += """
Extract and structure the data according to the schema. Return ONLY a valid JSON object that follows the schema, no other text.
If certain fields cannot be extracted, use null or appropriate empty values.
"""

        response = self.provider.generate_response(prompt, max_tokens=4000)

        if not response:
            return None

        try:
            # Extract JSON from response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]

            structured_data = json.loads(response.strip())
            return structured_data
        except json.JSONDecodeError as e:
            print(f"Failed to parse conversion JSON for {page_data['url']}: {e}")
            return None

    def convert_all_pages(
        self,
        scraped_data: List[Dict],
        schema: Dict,
        output_file: str,
        batch_size: int = 10,
        delay: float = 1.0
    ) -> List[Dict]:
        """
        Convert all scraped pages to structured JSON.

        Args:
            scraped_data: List of scraped page data
            schema: Target JSON schema
            output_file: Path to save the output JSON
            batch_size: Number of pages to process before saving
            delay: Delay between API calls in seconds

        Returns:
            List of structured data objects
        """
        print(f"Converting {len(scraped_data)} pages to structured JSON...")

        structured_data = []
        failed_urls = []

        for i, page_data in enumerate(scraped_data, 1):
            print(f"Processing page {i}/{len(scraped_data)}: {page_data['url']}")

            try:
                structured = self.convert_page_to_structured_data(page_data, schema)

                if structured:
                    # Add metadata
                    structured['_metadata'] = {
                        'source_url': page_data['url'],
                        'title': page_data['title'],
                        'scraped_at': page_data['fetched_at'],
                        'url_hash': page_data['url_hash']
                    }
                    structured_data.append(structured)
                else:
                    failed_urls.append(page_data['url'])
                    print(f"  Failed to convert page")

            except Exception as e:
                print(f"  Error processing page: {e}")
                failed_urls.append(page_data['url'])

            # Save progress periodically
            if i % batch_size == 0:
                self._save_output(output_file, structured_data)
                print(f"  Progress saved ({len(structured_data)} pages converted)")

            # Rate limiting
            if i < len(scraped_data):
                time.sleep(delay)

        # Final save
        self._save_output(output_file, structured_data)

        print(f"\nConversion complete!")
        print(f"Successfully converted: {len(structured_data)} pages")
        print(f"Failed: {len(failed_urls)} pages")

        if failed_urls:
            print(f"\nFailed URLs:")
            for url in failed_urls[:10]:
                print(f"  - {url}")
            if len(failed_urls) > 10:
                print(f"  ... and {len(failed_urls) - 10} more")

        return structured_data

    def _save_output(self, output_file: str, data: List[Dict]):
        """Save structured data to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """Example usage of the AIDataConverter."""
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Usage: python ai_converter.py <scraped_data.json> [provider] [output_file]")
        print("Providers: gemini (default), claude, openai")
        print("Example: python ai_converter.py ./scraped_data/json/scraped_data.json gemini output.json")
        return

    input_file = sys.argv[1]
    provider = sys.argv[2] if len(sys.argv) > 2 else "gemini"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "structured_data.json"

    # Load scraped data
    with open(input_file, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)

    print(f"Loaded {len(scraped_data)} pages from {input_file}")

    # Initialize converter
    converter = AIDataConverter(provider=provider)

    # Analyze data structure
    analysis = converter.analyze_data_structure(scraped_data)

    # Save analysis
    analysis_file = Path(output_file).parent / "schema_analysis.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"Schema analysis saved to: {analysis_file}")

    # Convert all pages
    schema = analysis.get('schema', {})
    if not schema:
        print("No schema generated, cannot convert data")
        return

    structured_data = converter.convert_all_pages(
        scraped_data,
        schema,
        output_file,
        batch_size=5,
        delay=2.0
    )

    print(f"\nStructured data saved to: {output_file}")


if __name__ == "__main__":
    main()
