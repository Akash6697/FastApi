from fastapi import APIRouter
from . import auth, templates

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(templates.router, prefix="/template", tags=["Templates"])
