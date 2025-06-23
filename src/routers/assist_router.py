from ..services.download_services import html_to_pdf_bytes, sanitize_filename
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from .dependencies import get_current_user
from ..models import PDFRequest
from urllib.parse import quote
import asyncio
import io
from fastapi import WebSocket, WebSocketDisconnect
from ..utils import websocket_manager
import logging
# Initialzing router
router = APIRouter()
logger = logging.getLogger(__name__)


# --- Protected API Endpoint for Generating PDF ---
@router.post("/generate-pdf")
async def generate_pdf_alt(
    data: PDFRequest, decoded_token: dict = Depends(get_current_user)
):
    """
    Receives the full HTML document (including your <style> blocks),
    and returns a streaming PDF response without touching disk.
    """

    user_uid = decoded_token.get("uid")
    user_email = decoded_token.get("email")

    html = data.html
    filename = data.filename
    try:
        # Sanitize the filename
        safe_filename = sanitize_filename(filename)

        # Generate PDF
        pdf_bytes = await asyncio.to_thread(html_to_pdf_bytes, html)

        # Create streaming response
        buffer = io.BytesIO(pdf_bytes)

        def iter_pdf():
            buffer.seek(0)
            for chunk in iter(lambda: buffer.read(8192), b""):
                yield chunk

        # Create safe filename for Content-Disposition header
        encoded_filename = quote(f"{safe_filename}.pdf")

        return StreamingResponse(
            iter_pdf(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=\"{safe_filename}.pdf\"; filename*=UTF-8''{encoded_filename}"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")




@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time communication with clients.
    """
    await websocket_manager.connect(user_id, websocket)
    
    try:
        while True:
            # Keep the connection alive and listen for any client messages
            # You can handle incoming messages here if needed
            data = await websocket.receive_text()
            logger.info(f"Received message from user {user_id}: {data}")
            
            # Optional: Echo back or handle the received message
            # await websocket.send_json({"type": "echo", "message": data})
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(user_id, websocket)
        logger.info(f"Client {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        websocket_manager.disconnect(user_id, websocket)
