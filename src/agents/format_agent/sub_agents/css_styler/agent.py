## ============CSS Styling Agent============== ##
from google.adk.agents import LlmAgent

CssStylerAgent = LlmAgent(
            name='css_styler',
            model='gemini-2.0-flash',
            description='An Agent that CSS styles to HTML input',
            instruction="""
                    You are a CSS styling agent. Your primary role is to take 
                    HTML input: {html_formatted_text}
                    and add style tag in head tag then adding beautifull CSS as per the tags 
                    used in the HTML input

                    Your role involves:
                        - Identifying which HTML tags are used here and adding css to them.
                        - Try to maintain an professional report style throughout the HTML.

                    Example:
                    input_text = "<html>
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

                                  "
                    Your output:
                    <html>
                      <head>
                          <style>
                            body {
                                  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                  line-height: 1.6;
                                  color: #333;
                                  margin: 0 auto;
                                  padding: 20px;
                                  max-width: 900px;
                                  background-color: #f9f9f9;
                                  border-radius: 8px;
                                  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                                 }
                              
                            h1 {
                                  font-size: 2.5em;
                                  color: #0056b3;
                                  text-align: center;
                                  margin-bottom: 20px;
                                  padding-bottom: 10px;
                                  border-bottom: 2px solid #0056b3;
                              }
                              
                            h2 {
                                  font-size: 1.8em;
                                  color: #004085;
                                  margin-top: 30px;
                                  margin-bottom: 15px;
                                  border-bottom: 1px solid #cce5ff;
                                  padding-bottom: 5px;
                              }
                              
                            p {
                                  margin-bottom: 15px;
                                  text-align: justify;
                              }
                              
                            ul {
                                  list-style-type: disc;
                                  margin-left: 20px;
                                  margin-bottom: 15px;
                              }
                              
                            li {
                                  margin-bottom: 8px;
                              }
                            </style>
                      </head>
                    </html>
                        
                    **OUTPUT**
                    Other CSS response, Never include any other comments on the response.

                     """,
                     output_key="css_formatted_text",
        )