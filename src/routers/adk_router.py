from fastapi import APIRouter, HTTPException, Depends
import logging
from ..models import (
    AgentQueryRequest,
    AgentResponse,
    DelegateAgentResponse,
    DelegateAgentQueryRequest,
)
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from .dependencies import get_current_user, get_db_session_service
from ..agents.format_agent.agent import FormatAgentOrchestrator
from ..agents.chatbox_agent.agent import ChatAgentOrchestrator
from google.genai import types
import os
from dotenv import load_dotenv
from ..utils import clean_html_response, is_approval, websocket_manager
import uuid
from datetime import datetime
import json
from typing import Optional
from pydantic import ValidationError
from google.adk.events import Event, EventActions
import time
import re
def clean_json_block(raw: str) -> str:
    # Remove triple backticks and optional language hint (like ```json)
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    return cleaned


edits_dict = {}

load_dotenv()
# setting up Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
# important to use logger.setLevel() in production


# Initializing the Orchestrator
Format_Agent_Instance = FormatAgentOrchestrator()
Delegate_Agent_Instance = ChatAgentOrchestrator()

router = APIRouter()

APP_NAME = "DraftFlow"

# --- New Function: Send agent suggestion via WebSocket ---
async def send_agent_suggestion_via_websocket(user_id: str, block_id: str, revised_text: str):
    """
    Sends an agent's suggestion message to the frontend via WebSocket.
    """
    await websocket_manager.send_personal_message(user_id, {
        "type": "agent_suggestion",
        "block_id": block_id,
        "revised_text": revised_text,
    })



# Format Agent Endpoint
@router.post("/format", response_model=AgentResponse)
async def query_agent_endpoint(
    request_body: AgentQueryRequest,
    decoded_token: dict = Depends(get_current_user),  # Protect this endpoint
    session_service: DatabaseSessionService = Depends(get_db_session_service),
):
    """
    Endpoint to interact with the multi-agent ADK system.
    request_body: {"query": "Hello, Tell me a joke related to python"}
    """
    user_id: str = str(decoded_token.get("uid") or "Anonymous_User ")
    user_email = decoded_token.get("email")
    user_query = request_body.query
    # session_id = request_body.session_id if request_body.session_id else user_id
    session_id = user_id

    logger.info(
        f"User {user_email} (UID: {user_id}) queried ADK with: '{user_query}' (Session: {session_id})"
    )

    try:
        # Retrieve the globally initialized session service from the app state
        # session_service: DatabaseSessionService = app.state.session_service

        # --- Session Service ---

        # Attempt to retrieve an existing session for the given user_id and session_id.
        current_session = None
        try:
            current_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id,
            )
        except Exception as e:
            logger.warning(
                f"Existing Session retrieval failed for session_id='{session_id}' "
                f"and user_uid='{user_id}': {e}"
            )

        # If no session found, creating new session
        if current_session is None:
            logger.info(f"Creating new session for '{session_id}'")
            current_session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id,
            )
        else:
            logger.info(
                f"Existing session '{session_id}'has been found. Resuming session."
            )

        # --- Initialize the ADK Runner ---
        runner = Runner(
            app_name=APP_NAME,
            agent=Format_Agent_Instance.root_agent,
            session_service=session_service,
        )

        # --- Initialize the Agent ---
        user_message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_query)]
        )

        final_response_text = "No response from the Agent"

        # To run the agent asynchronously
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        )

        # Iterate through the events yielded by the agent's execution to find the final response.
        last_event_content = None
        async for event in events:
            logger.info(f"Received event from ADK: {event.author} ")
            if event.is_final_response():
                if event.content and event.content.parts:
                    last_event_content = event.content.parts[0].text

        if last_event_content:
            final_response_text = clean_html_response(last_event_content)
        else:
            logger.error("No final response event found from the Sequential Agent.")

        logger.info("====Session Event Exploration====")
        session_after_run = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        if session_after_run is not None:
            logger.debug(f"--- Examining Session Properties ---")
            logger.debug(f"ID (`id`):                {session_after_run.id}")
            logger.debug(f"Application Name (`app_name`): {session_after_run.app_name}")
            logger.debug(f"User ID (`user_id`):         {session_after_run.user_id}")
            logger.debug(f"State (`state`):          {session_after_run.state}")
            logger.debug(
                f"Events (`events`):         {session_after_run.events}"
            )  # Initially empty
            logger.debug(
                f"Last Update (`last_update_time`): {session_after_run.last_update_time:.2f}"
            )
            logger.debug(f"---------------------------------")
        else:
            logger.warning(
                "session_after_run is None; cannot log session properties or state."
            )

        logger.info("====Final Session State====")
        for key, value in session_after_run.state.items():  # type: ignore
            logger.debug(f"{key}: {value}")

        return AgentResponse(status="success", response_text=final_response_text)

    except Exception as e:
        logger.error(f"Error querying ADK agent: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to process agent query: {e}"
        )


# ChatBox Agent Endpoint
@router.post("/delegate", response_model=DelegateAgentResponse)
async def delegate_agent_endpoint(
    request_body: DelegateAgentQueryRequest,
    decoded_token: dict = Depends(get_current_user),
    session_service: DatabaseSessionService = Depends(get_db_session_service),
):
    """
    Endpoint to interact with the multi-agent ADK system.
    """
    # 0. Extract & validate inputs early
    try:
        # Initialize the dictionary to store edits
        original_text = request_body.original_text
        user_query = request_body.user_query
        user_selected = request_body.userSelectedText
        block_id = request_body.dataBlockId
        block_content = request_body.blockContent
    except Exception as e:
        logger.error("Malformed request body", exc_info=True)
        raise HTTPException(400, detail="Invalid request body")

    # 1. Build session_id
    user_id = str(decoded_token.get("uid", "Anonymous"))
    session_id = f"session_{user_id}_{datetime.utcnow():%Y%m%d%H%M%S}_{uuid.uuid4().hex[:6]}"
    logger.info(f"Starting delegate for user={user_id} session={session_id!r}")

    try:
        # 2. Load or create session
        try:
            current_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id)
        except Exception as e:
            logger.warning("Failed to load session, creating new one", exc_info=True)
            current_session = None

        if current_session is None:
            current_session = await session_service.create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id)
            logger.info("Created new session")
        else:
            logger.info("Resumed existing session")

        # 3. Approval branch
        if is_approval(str(user_query)):
            logger.info("User approval detected")
            pending = edits_dict.get("pending_edit")
            print("Printing the pending")
            print(pending)
            if not pending:
                raise HTTPException(400, detail="Nothing pending to approve")
            
            to_block = pending.get("block_id")
            to_text = pending.get("revised_text")
            print(to_block)
            print(to_text)
            if not (to_block and to_text):
               raise HTTPException(500, detail="Pending edit data is malformed")

            # send update over WS (ensure await if coroutine)
            await send_agent_suggestion_via_websocket(user_id, to_block, to_text)

            # clear pending in DBif "pending_edit" in edits_dict:
            if "pending_edit" in edits_dict:
                del edits_dict["pending_edit"]


            return DelegateAgentResponse(
                status="success",
                response_message="Changes applied",
                revised_text=to_text,
                dataBlockId=to_block
            )

        # 4. Initialize ADK runner
        try:
            runner = Runner(
                app_name=APP_NAME,
                agent=Delegate_Agent_Instance.root_agent,
                session_service=session_service,
            )
        except Exception as e:
            logger.error("Runner init failed", exc_info=True)
            raise HTTPException(500, detail="Server error initializing agent")

        # 5. Run agent and collect last response
        input_payload = {
            "original_text": original_text,
            "user_query": user_query,
            "userSelectedText": user_selected,
            "dataBlockId": block_id,
            "blockContent": block_content
        }
        message = types.Content(role="user", parts=[types.Part.from_text(text=json.dumps(input_payload))])

        try:
            events = runner.run_async(user_id=user_id, session_id=session_id, new_message=message)
        except Exception as e:
            logger.error("Agent start failed", exc_info=True)
            raise HTTPException(502, detail="Failed to dispatch to agent")

        last_event = None
        async for ev in events:
            if ev.is_final_response():
                if ev.content and ev.content.parts:
                    last_event = ev.content.parts[0].text

        #if not last_event or not last_event.content or not last_event.content.parts:
         #   logger.error("No final agent response received")
          #  raise HTTPException(504, detail="Agent did not return a response")

        # 6. Parse agent response JSON
        try:
            raw = clean_json_block(str(last_event)) 
            if raw is None:
                logger.error("Agent response text is None")
                raise HTTPException(502, detail="Agent returned empty response")
            print(raw)
            parsed = DelegateAgentResponse.model_validate(json.loads(raw))
        except json.JSONDecodeError:
            logger.error("Agent returned invalid JSON", exc_info=True)
            raise HTTPException(502, detail="Malformed JSON from agent")
        except ValidationError as e:
            logger.error("Agent response failed Pydantic validation", exc_info=True)
            raise HTTPException(502, detail="Unexpected agent response format")

        # 7. Store pending edit if provided
        if parsed.revised_text and parsed.dataBlockId:
            delta = {
                    "block_id": parsed.dataBlockId,
                    "revised_text": parsed.revised_text
            }
            edits_dict["pending_edit"] = delta 
            print("The dict is here")
            print(edits_dict)
            
            logger.info("Stored pending edit in session")

        # 8. Return final response
        return DelegateAgentResponse(
            status="success",
            response_message=parsed.response_message,
            revised_text=parsed.revised_text,
            dataBlockId=parsed.dataBlockId
        )

    except HTTPException:
        # re-raise HTTPExceptions directly
        raise
    except Exception as e:
        logger.error("Unhandled exception in delegate endpoint", exc_info=True)
        raise HTTPException(500, detail="Internal server error")
