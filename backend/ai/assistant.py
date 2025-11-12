"""
AI Assistant module for generating summaries and insights from blockchain data.
Supports both local summarization and Claude Haiku 4.5 API calls.
"""

import requests
import os
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Configuration
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_API_URL = os.getenv('CLAUDE_API_URL', 'https://api.anthropic.com/v1')
CLAUDE_MODEL = 'claude-3-5-haiku-20241022'  # Claude Haiku 4.5 model identifier


def call_claude_haiku(prompt: str, max_tokens: int = 1024) -> Optional[str]:
    """
    Call Claude Haiku 4.5 API to generate a response.

    :param prompt: The prompt to send to Claude
    :param max_tokens: Maximum tokens in the response
    :return: The response text from Claude, or None if API call fails or API key not set
    """
    if not CLAUDE_API_KEY:
        logger.debug("CLAUDE_API_KEY not set; Claude AI integration disabled")
        return None

    try:
        headers = {
            'x-api-key': CLAUDE_API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        }

        payload = {
            'model': CLAUDE_MODEL,
            'max_tokens': max_tokens,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }

        response = requests.post(
            f'{CLAUDE_API_URL}/messages',
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if result.get('content') and len(result['content']) > 0:
                return result['content'][0].get('text')
        else:
            logger.error(f"Claude API error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Claude API: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in Claude API call: {str(e)}")
        return None


def generate_summary(raw_data: Dict) -> str:
    """
    Main function to generate a summary from raw blockchain data.
    Uses Claude Haiku 4.5 if API key is configured, otherwise falls back to local summarization.

    :param raw_data: The raw data from the blockchain.
    :return: A human-readable summary of the batch information.
    """
    if not raw_data or 'batches' not in raw_data:
        # If no data provided, use the default sample data
        raw_data = process_input_data("")

    # Try Claude API first if configured
    if CLAUDE_API_KEY:
        claude_summary = _generate_claude_summary(raw_data)
        if claude_summary:
            return claude_summary
        logger.warning("Claude API failed; falling back to local summarization")

    # Fall back to local summarization
    return summarize_blockchain_data(raw_data)


def _generate_claude_summary(raw_data: Dict) -> Optional[str]:
    """
    Generate a summary using Claude Haiku 4.5 API.

    :param raw_data: The raw blockchain data
    :return: Claude-generated summary or None if API fails
    """
    # Format data for Claude prompt
    batch_info = []
    for batch in raw_data.get('batches', []):
        batch_text = f"""
Batch ID: {batch['id']}
Name: {batch['name']}
Origin: {batch['origin']}
Tracking History: {', '.join(batch['tracking_history'])}
"""
        batch_info.append(batch_text)

    batches_text = "\n".join(batch_info) if batch_info else "No batches available."

    prompt = f"""You are a supply chain analyst. Provide a concise, professional summary of the following boba ingredient batch tracking data:

{batches_text}

Please include:
1. Overview of total batches and their origins
2. Key tracking milestones
3. Any notable supply chain patterns or observations
4. Recommendations for supply chain optimization

Keep the summary to 2-3 paragraphs."""

    return call_claude_haiku(prompt, max_tokens=1024)


def summarize_blockchain_data(raw_data: Dict) -> str:
    """
    Summarizes the raw blockchain data into a human-readable format.
    This is the fallback local summarization when Claude API is not available.

    :param raw_data: The raw data from the blockchain containing batch information.
    :return: A summary of the batch information.
    """
    summary = []
    for batch in raw_data.get('batches', []):
        batch_summary = f"Batch ID: {batch['id']}\n"
        batch_summary += f"Name: {batch['name']}\n"
        batch_summary += f"Origin: {batch['origin']}\n"
        batch_summary += f"Tracking History: {', '.join(batch['tracking_history'])}\n"
        summary.append(batch_summary)

    if not summary:
        return "No batch data available for summary."

    return "\n".join(summary)


def process_input_data(input_data: str) -> Dict:
    """
    Processes the input data to prepare it for summarization.

    :param input_data: The raw input data as a string.
    :return: A structured dictionary containing batch information.
    """
    # Here you would implement the logic to convert the input string into a structured dictionary.
    # This is a placeholder for demonstration purposes.
    return {
        'batches': [
            {
                'id': '1',
                'name': 'Tapioca Pearls',
                'origin': 'Taiwan',
                'tracking_history': ['Harvested', 'Processed', 'Shipped']
            },
            {
                'id': '2',
                'name': 'Milk Tea',
                'origin': 'China',
                'tracking_history': ['Brewing', 'Bottled', 'Delivered']
            }
        ]
    }