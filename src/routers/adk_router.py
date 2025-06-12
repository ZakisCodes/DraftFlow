from fastapi import APIRouter, HTTPException, Depends
import logging
from ..models import AgentQueryRequest, AgentResponse
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from .dependencies import get_current_user, get_db_session_service
from ..agents.format_agent.agent import FormatAgentOrchestrator
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
# setting up Logger
logging.basicConfig(
    filename='Adk_logs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# important to use logger.setLevel() in production


# Initializing the Orchestrator
Format_Agent_Instance = FormatAgentOrchestrator()

router = APIRouter()

APP_NAME = "DraftFlow"
# Format Agent Endpoint
@router.post("/format", response_model=AgentResponse)
async def query_agent_endpoint(
    request_body: AgentQueryRequest,
    decoded_token: dict = Depends(get_current_user), # Protect this endpoint
    session_service: DatabaseSessionService = Depends(get_db_session_service)
):
    """
    Endpoint to interact with the multi-agent ADK system.
    request_body: {"query": "Hello, Tell me a joke related to python"}
    """
    user_id: str = str(decoded_token.get("uid") or "Anonymous_User ")
    user_email = decoded_token.get("email")
    user_query = request_body.query
    #session_id = request_body.session_id if request_body.session_id else user_id
    session_id = user_id
    
    logger.info(f"User {user_email} (UID: {user_id}) queried ADK with: '{user_query}' (Session: {session_id})")

    try:
        # Retrieve the globally initialized session service from the app state
        #session_service: DatabaseSessionService = app.state.session_service
        
        # --- Session Service ---
        
        # Attempt to retrieve an existing session for the given user_id and session_id.
        current_session = None
        try:
            current_session = await session_service.get_session(
                app_name=APP_NAME,
                user_id = user_id,
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
            logger.info(f"Existing session '{session_id}'has been found. Resuming session.")
        

        # --- Initialize the ADK Runner ---
        runner = Runner(
            app_name=APP_NAME,
            agent=Format_Agent_Instance.root_agent,
            session_service = session_service,
        )

        # --- Initialize the Agent ---
        user_message = types.Content(
            role="user", parts=[types.Part.from_text(text=user_query)]
        )

        final_response_text = "No response from the Agent"

        # To run the agent asynchronously
        events = runner.run_async(
            user_id = user_id,
            session_id = session_id,
            new_message = user_message,
        )

        # Iterate through the events yielded by the agent's execution to find the final response.
        last_event_content = None
        async for event in events:
            logger.info(f"Received event from ADK: {event.author} ")
            if event.is_final_response():
                if event.content and event.content.parts:
                    last_event_content = event.content.parts[0].text


        if last_event_content:
            final_response_text=last_event_content
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
            logger.debug(f"Events (`events`):         {session_after_run.events}") # Initially empty
            logger.debug(f"Last Update (`last_update_time`): {session_after_run.last_update_time:.2f}")
            logger.debug(f"---------------------------------")
        else:
            logger.warning("session_after_run is None; cannot log session properties or state.")

        
        logger.info("====Final Session State====")
        for key, value in session_after_run.state.items(): # type: ignore
            logger.debug(f"{key}: {value}")   

        return AgentResponse(
            status="success",
            response_text=final_response_text
        )

    except Exception as e:
        logger.error(f"Error querying ADK agent: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process agent query: {e}")