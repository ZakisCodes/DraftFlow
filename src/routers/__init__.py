from fastapi import APIRouter
from .ui_router import router as ui_router
from .assist_router import router as assist_router
from .auth_router import router as auth_router
from .adk_router import router as adk_router
router = APIRouter()

router.include_router(ui_router,  prefix="", tags=["UI Pages"])
router.include_router(assist_router,  prefix="/api", tags=["AI Assistance"])
router.include_router(adk_router,  prefix="/adk", tags=["ADK API's"])
router.include_router(auth_router,  prefix="/auth", tags=["Authentication"])
#router.include_router(upload_router,  prefix="/upload", tags=["File Upload"])
#router.include_router(feedback_router,  prefix="/feedback", tags=["Feedback"])