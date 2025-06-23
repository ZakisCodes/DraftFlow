import re

def clean_html_response(response_text: str) -> str:
    """
    Clean HTML response by removing markdown code block wrapping.
    
    Args:
        response_text: The raw response from the LLM
        
    Returns:
        Clean HTML content without markdown formatting
    """
    if not response_text:
        return response_text
    
    # Remove markdown code block wrapping (```html ... ```)
    # This pattern handles various cases:
    # - ```html\n<html>...</html>\n```
    # - ```\n<html>...</html>\n```
    # - ```html<html>...</html>```
    
    # Pattern to match markdown code blocks
    markdown_pattern = r'^```(?:html)?\s*\n?(.*?)\n?```\s*$'
    
    # Try to match and extract the HTML content
    match = re.match(markdown_pattern, response_text.strip(), re.DOTALL)
    
    if match:
        # Extract the HTML content from the markdown block
        html_content = match.group(1)
        return html_content.strip()
    
    # If no markdown wrapping found, return as-is
    return response_text.strip()

# Alternative approach using simple string operations
def clean_html_response_simple(response_text: str) -> str:
    """
    Simple approach to clean HTML response.
    """
    if not response_text:
        return response_text
    
    text = response_text.strip()
    
    # Remove opening markdown block
    if text.startswith('```html'):
        text = text[7:]  # Remove '```html'
    elif text.startswith('```'):
        text = text[3:]  # Remove '```'
    
    # Remove closing markdown block
    if text.endswith('```'):
        text = text[:-3]  # Remove closing '```'
    
    return text.strip()

# Usage in your router:
"""
# Add this import at the top of your adk_router.py
from .utils import clean_html_response  # Adjust import path as needed

# Then modify your router code:
if last_event_content:
    # Clean the response to remove any markdown formatting
    final_response_text = clean_html_response(last_event_content)
    logger.debug(f"Cleaned HTML response: {final_response_text[:100]}...")  # Log first 100 chars
else:
    logger.error("No final response event found from the Sequential Agent.")
"""