from fastapi import APIRouter, Depends, HTTPException, status
from .auth import get_current_user
from .crud import create_template, get_all_templates, get_template, update_template, delete_template
from .models import NewTemplateCreate, TemplateUpdate, Template
from bson import ObjectId
from .models import User


router = APIRouter()


@router.post("/", response_model=Template)
async def create_new_template(template: NewTemplateCreate, user: User = Depends(get_current_user)):
    return create_template(template)


@router.get("/", response_model=list[Template])
async def get_all_template(user: User = Depends(get_current_user)):
    return get_all_templates()


@router.get("/{template_id}", response_model=Template)
async def get_single_template(template_id: str, user: User = Depends(get_current_user)):
    return get_template(template_id)


@router.put("/{template_id}", response_model=Template)
async def update_single_template(template_id: str, template: TemplateUpdate, user: User = Depends(get_current_user)):
    return update_template(template_id, template)


@router.delete("/{template_id}")
async def delete_single_template(template_id: str, user: User = Depends(get_current_user)):
    delete_template(template_id)
    return {"message": "Template deleted successfully"}
