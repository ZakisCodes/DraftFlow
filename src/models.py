from pydantic import BaseModel, Field
from typing import Optional


# Define a Pydantic model for the request body
class AgentQueryRequest(BaseModel):
    query: str


# session_id: Optional[str] = None # For maintaining session state across queries

# Agent Return structure
class AgentResponse(BaseModel):
    status: str
    response_text: Optional[str]


class PDFRequest(BaseModel):
    html: str
    filename: str
    
class DelegateAgentResponse(BaseModel):
    status: str = Field(..., description="Status of the operation (e.g., 'success', 'failure').")
    response_message: str = Field(..., description="A user-friendly message about the operation's outcome.")
    revised_text: Optional[str] = Field(None, description="The processed or revised text, if applicable.")
    dataBlockId: Optional[str]

class DelegateAgentQueryRequest(BaseModel):
    original_text: Optional[str] 
    user_query:  Optional[str]
    userSelectedText : Optional[str]
    dataBlockId: Optional[str]
    blockContent: Optional[str]