from pydantic import BaseModel
from typing import Optional


# Define a Pydantic model for the request body
class AgentQueryRequest(BaseModel):
    query: str


# session_id: Optional[str] = None # For maintaining session state across queries


# Experimental purposes model
class GenerateTextRequest(BaseModel):
    input_text: str


# Agent Return structure
class AgentResponse(BaseModel):
    status: str
    response_text: Optional[str]


class PDFRequest(BaseModel):
    html: str
    filename: str
