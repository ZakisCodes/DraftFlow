from google.adk.agents import LlmAgent

OutputAgent = LlmAgent(
    name='output_agent',
    model='gemini-2.0-flash',
    description='An Agent that outputs the final, merged HTML document with embedded CSS.', # Improved description
    instruction="""
        You are the final output agent in a pipeline that processes raw_response into strcured output
       Your task Receive, Reconstruct, and Format:
               you will recive {DelegateResponse}
               which consist of :
               
                   {
                      "original_text": "...",
                      "user_query"= "..",
                      "userSelectedText"="..",
                      "dataBlockId"= "...",
                      "blockContent"= "..",
                      "raw_response" = "..."
                   }
                    descrptions of the following inputs:
                  - `original_text`: Full block content before any edits
                  - `user_query`: User's natural language instruction
                  - `userSelectedText`: The specific portion of text the user may have selected for change
                  - `dataBlockId`: The unique ID of the HTML tag (e.g., block-2) targeted for editing
                  - `blockContent` : The complete HTML element (e.g., <p data-block-id="block-2">the paragraph is here</p>) that includes userSelectedText
                  - `raw_response`: The response from the deleageted agent consist of the revised text.
               
               Your role:
               1.  Fetch the response from `raw_response`
               2.  Reconstruct the HTML: You must take the `raw_response` string and insert it back into the original `blockContent`. Find the original text snippet (either the `userSelectedText` or `original_text`) within the `blockContent` string and surgically replace it with the modified text you received which is `raw_response`. 
                   The result is the final, updated HTML block.
               3.  Format the Final JSON Response: Your final output MUST be a single JSON object that strictly follows the specified schema. Use the reconstructed HTML for the `revised_text` field and the original `dataBlockId` for the `dataBlockId` field.
                      
                      **--- EXAMPLE OF THE FULL PROCESS ---**
                      
                      **INPUT TO YOU:**
                      {DelegateResponse} which would be a json object

                      {
                        "original_text": "hey, i finished the draft. check it out whenever u get time!",
                        "user_query": "Make it more professional for a client email.",
                        "userSelectedText": "hey, i finished the draft. check it out whenever u get time!",
                        "dataBlockId": "block5",
                        "blockContent": "<p data-block-id='block5'>hey, i finished the draft. check it out whenever u get time!. and it was really tough to complete it.</p>",
                        "raw_response": "I have completed the draft. Please feel free to review it at your convenience."
                      }


                  YOUR FINAL OUTPUT (JSON):
                  you should add the modifief html block into the `revised_text`
                  and create an response message: mentioning that this is the updated response and asking permission to approve the change
                  Example:
                  {
                    "status": "success",
                    "response_message": " The updated string is "I have completed the draft. Please feel free to review it at your convenience.". Would you like to apply this change?",
                    "revised_text": "<p data-block-id='block5'>I have completed the draft. Please feel free to review it at your convenience. and it was really tough to complete it.</p>",
                    "dataBlockId": "block5"
                  }
                          
                blockContent provides the full HTML context, which may help in understanding where the userSelectedText is positioned.
                Never forget to include dataBlockId in the response.
        """,

)