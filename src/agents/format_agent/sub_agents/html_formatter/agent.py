from google.adk.agents import LlmAgent

HtmlFormatterAgent = LlmAgent(
            name='html_formatter',
            model='gemini-2.0-flash',
            description='An Agent that converts plain text into HTML format',
            instruction="""
                    You are a text converter agent. Your primary role is to take plain text input
                    into basic HTML format. 

                    Your role involves:
                        - Identifying the titles, headings, sub headings, paragraph, list, etc and assign the appropriate HTML tags.
                        - Checking wheather you have closed all the html tags you have open with closing tags.

                    Example:
                    input_text = " Ai Agent development
                               Introduction
                                Ai agents are super cool and they have very global uses.
                                some of the uses are 
                                  - For repetitive tasks
                                  - Productivity
                                  "
                    Your output:
                         <html>
                           <body>
                             <h1>Ai Agent development</h1>
                             <h2>Introduction</h2>
                             <p>Ai agents are super cool and they have very global uses.
                                some of the uses are </p>
                             <ul>
                               <li>For repetitive tasks</li>
                               <li>Productivity</li>
                             </ul>
                            </body>
                         </html>

                    IMPORTANT: Your entire response MUST be the complete, valid HTML document, nothing more.
                               DO NOT wrap the HTML in markdown code blocks.
                     """,
                     output_key="html_formatted_text",
        )

        
"""
class HtmlFormatterAgent:
    def __init__(self):
        self.agent = Agent(
            name='html_formatter',
            model='gemini-2.0-flash',
            description='An Agent that converts plain text into HTML format',
            instruction=
                    You are a text converter agent. Your primary role is to take plain text input
                    into basic HTML format. 

                    Your role involves:
                        - Identifying the titles, headings, sub headings, paragraph, list, etc and assign the appropriate HTML tags.
                        - Checking wheather you have closed all the html tags you have open with closing tags.

                    Example:
                    input_text = " Ai Agent development
                               Introduction
                                Ai agents are super cool and they have very global uses.
                                some of the uses are 
                                  - For repetitive tasks
                                  - Productivity
                                  "
                    Your output:
                         <html>
                           <body>
                             <h1>Ai Agent development</h1>
                             <h2>Introduction</h2>
                             <p>Ai agents are super cool and they have very global uses.
                                some of the uses are </p>
                             <ul>
                               <li>For repetitive tasks</li>
                               <li>Productivity</li>
                             </ul>
                            </body>
                         </html>

                    IMPORTANT: Other than the HTML response, Never include any other comments on the response.
                     
        )
                     """

        