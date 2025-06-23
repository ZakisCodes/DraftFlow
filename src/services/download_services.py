# main.py
from fastapi.responses import StreamingResponse
import asyncio
import io
import logging
from typing import Optional
from weasyprint import HTML
from bs4 import BeautifulSoup
import re
# Configure logging
logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to be safe for download.
    Removes/replaces unsafe characters and limits length.
    """
    if not filename:
        return "export"
    
    # Remove or replace unsafe characters
    # Keep only alphanumeric, spaces, hyphens, underscores, and periods
    sanitized = re.sub(r'[^\w\s\-\.]', '', filename)
    
    # Replace multiple spaces with single space and strip
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Replace spaces with underscores for better compatibility
    sanitized = sanitized.replace(' ', '_')
    
    # Limit length to reasonable size
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    # Ensure it's not empty after sanitization
    if not sanitized:
        sanitized = "export"
    
    return sanitized

# Alternative using bleach for even stronger sanitization (requires: pip install bleach)
def sanitize_html(html: str) -> str:
    """
    Alternative sanitization using bleach library (whitelist approach).
    This is more restrictive but potentially safer.
    
    Args:
        html (str): HTML content to sanitize
        
    Returns:
        str: Sanitized HTML content
    """
    try:
        import bleach
        from bleach.css_sanitizer import CSSSanitizer
    except ImportError:
        raise ImportError("bleach library required: pip install bleach")
    
    # Define allowed tags (whitelist approach)
    allowed_tags = [
        'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'strike', 'sup', 'sub',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'dl', 'dt', 'dd',
        'div', 'span', 'blockquote', 'pre', 'code',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'hr', 'img', 'a', 'style'
    ]
    
    # Define allowed attributes per tag
    allowed_attributes = {
        '*': ['class', 'id', 'style'],  # Global attributes
        'img': ['src', 'alt', 'width', 'height', 'title'],
        'a': ['href', 'title', 'target'],
        'table': ['border', 'cellpadding', 'cellspacing', 'width'],
        'th': ['colspan', 'rowspan', 'scope'],
        'td': ['colspan', 'rowspan'],
        'div': ['align'],
        'p': ['align'],
        'style': []
    }
    
    # Define allowed protocols for links and images
    allowed_protocols = ['http', 'https', 'mailto', 'data']
    
    # Define CSS sanitizer for safe styling
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=[
            'color', 'background-color', 'background', 'border',
            'font-size', 'font-weight', 'font-style', 'font-family',
            'text-align', 'text-decoration', 'text-transform',
            'margin', 'margin-top', 'margin-bottom', 'margin-left', 'margin-right',
            'padding', 'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
            'width', 'height', 'max-width', 'max-height', 'min-width', 'min-height',
            'display', 'float', 'clear', 'position', 'top', 'bottom', 'left', 'right',
            'line-height', 'vertical-align', 'list-style', 'list-style-type'
        ]
    )
    
    return bleach.clean(
        text=html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=allowed_protocols,
        strip=True,
        strip_comments=True,
        css_sanitizer=css_sanitizer
    )


def html_to_pdf_bytes(html: str, base_url: Optional[str] = None) -> bytes:
    """
    Convert sanitized HTML content to PDF bytes.
    
    This function:
    1. Sanitizes the input HTML to remove dangerous content
    2. Renders the HTML to PDF using WeasyPrint
    3. Returns the PDF as bytes
    
    Args:
        html (str): HTML content to convert
        base_url (Optional[str]): Base URL for resolving relative links
        
    Returns:
        bytes: PDF content as bytes
        
    Raises:
        ValueError: If HTML is invalid or PDF generation fails
        RuntimeError: If WeasyPrint encounters rendering issues
    """
    if not html or not isinstance(html, str):
        raise ValueError("HTML content must be a non-empty string")
    
    try:
        # Step 1: Sanitize the HTML
#        logger.info("Sanitizing HTML content")
 #       clean_html = sanitize_html(html)
        
        # Step 2: Generate PDF
        logger.info("Converting HTML to PDF")
        pdf_buffer = io.BytesIO()
        
        # Create HTML object with optional base URL
        html_obj = HTML(string=html, base_url=base_url)
        
        # Render to PDF
        html_obj.write_pdf(target=pdf_buffer)
        
        # Get the PDF bytes
        pdf_bytes = pdf_buffer.getvalue()
        
        # Clean up
        pdf_buffer.close()
        
        if not pdf_bytes:
            raise RuntimeError("PDF generation resulted in empty output")
        
        logger.info(f"Successfully generated PDF ({len(pdf_bytes)} bytes)")
        return pdf_bytes
        
    except ValueError:
        # Re-raise ValueError from sanitization
        raise
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise RuntimeError(f"Failed to generate PDF: {str(e)}")

