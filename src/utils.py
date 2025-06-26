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

approval_keywords = [
    "yes", "yeah", "yep", "yup", "okay", "ok", "sure", "of course", "absolutely",
    "do it", "go ahead", "looks good", "sounds good", "apply that", 
    "let's do it", "i like that", "i agree", "that's better", "change it", "update it",
    "that's perfect", "i want that", "please do", "fine by me", "i approve", "love it",
    "that's great", "works for me", "lets use it", "exactly what i meant", "perfect"
]

def is_approval(text: str) -> bool:
    """
    Determines if the user input implies approval or consent
    to apply a previous suggestion using keyword group detection.
    """

    if not text:
        return False

    text = text.lower().strip()

    approval_keywords = [ "yes", "yeah", "approve"]

    # Partial match against approval phrases
    for phrase in approval_keywords:
        if phrase in text:
            return True

    # Regex patterns for more complex matches
    approval_patterns = [
        r"\b(yes|okay|ok|sure|please|go ahead|do it|apply it|looks good)\b",
        r"\bi (like|approve|agree|love|want|prefer) (that|this|it)\b",
        r"\blet'?s (go with|use|do|try) (that|it|this)\b",
    ]

    for pattern in approval_patterns:
        if re.search(pattern, text):
            return True

    return False



# managers/websocket_manager.py (Create this new file)
from fastapi import WebSocket
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages active WebSocket connections for users."""
    def __init__(self):
        # A dictionary mapping user_id to a list of active WebSocket connections for that user.
        # A user might have multiple tabs/devices open.
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """Registers a new WebSocket connection."""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"🔌 WebSocket connected for user: {user_id}. Total connections for user: {len(self.active_connections[user_id])}")

    def disconnect(self, user_id: str, websocket: WebSocket):
        """Removes a closed WebSocket connection."""
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                if not self.active_connections[user_id]: # If list becomes empty, remove user_id
                    del self.active_connections[user_id]
            except ValueError:
                logger.warning(f"WebSocket not found for user {user_id} during disconnect.")
        logger.info(f"🔌 WebSocket disconnected for user: {user_id}.")
        logger.info(f"Total active users: {len(self.active_connections)}. User {user_id} has {len(self.active_connections.get(user_id, []))} connections left.")


    async def send_personal_message(self, user_id: str, message: dict):
        """Sends a JSON message to all active WebSocket connections for a given user."""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id} via WebSocket: {e}. Removing broken connection.")
                    # In a real app, you might want to proactively remove this connection
                    # For simplicity, we'll let the disconnect method handle it when it fails for real
            logger.info(f"✅ Message sent to user {user_id} via WebSocket: {message['type']}")
        else:
            logger.warning(f"❌ No active WebSocket connections found for user: {user_id}. Message not sent: {message['type']}")
            print("Error is here")

# Instantiate the manager globally (or as a dependency if preferred)
websocket_manager = WebSocketManager()






