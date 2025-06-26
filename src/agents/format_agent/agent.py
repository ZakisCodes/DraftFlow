from .sub_agents import HtmlFormatterAgent as html_formatter, CssStylerAgent as css_styler, OutputAgent
from google.adk.agents import SequentialAgent

class FormatAgentOrchestrator:
    def __init__(self):
        # Root Agent
        self.root_agent = SequentialAgent(
            name='HtmlFormatPipeline',
            sub_agents=[html_formatter ,css_styler,OutputAgent],
            description="An pipeline that converts a raw text into HTML format and Give CSS Styling",
        )