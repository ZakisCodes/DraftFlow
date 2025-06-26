
from google.adk.tools.tool_context import ToolContext
import html
from google.adk.tools import FunctionTool
def convert_text_to_html_func(text_to_convert: str, tool_context: ToolContext) -> dict:
    """
    Converts plain text to a basic HTML format.
    - Replaces newlines with <br>.
    - Escapes HTML special characters.
    """
    print(f"--- Tool: convert_text_to_html_func called for text: '{text_to_convert[:50]}...' ---")

    # Escape HTML special characters first
    escaped_text = html.escape(text_to_convert)

    # Replace newlines with <br> tags for HTML
    html_output = escaped_text.replace('\n', '<br>')

    # You could add more sophisticated HTML wrapping here if needed,
    # e.g., <p> tags, <div>s, etc.
    final_html = f"<p>{html_output}</p>"

    # Optionally, update state with the last converted text
    tool_context.state["last_converted_text"] = text_to_convert
    tool_context.state["last_converted_html"] = final_html

    return {
        "status": "success",
        "original_text": text_to_convert,
        "html_output": final_html
    }

# Create the Tool instance
convert_text_to_html = FunctionTool(convert_text_to_html_func)

