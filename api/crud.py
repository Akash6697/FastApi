from pymongo import MongoClient
from bson import ObjectId
from settings import DATABASE_URL
from .models import TemplateCreate, TemplateUpdate, Template

client = MongoClient(DATABASE_URL)
db = client.get_database()
templates_collection = db['templates']

def create_template(template_data: TemplateCreate) -> Template:
    template_dict = template_data.dict()
    template_id = templates_collection.insert_one(template_dict).inserted_id
    return {**template_data.dict(), "id": str(template_id)}

def get_all_templates() -> list[Template]:
    templates = list(templates_collection.find())
    return [Template(id=str(template['_id']), **template) for template in templates]

def get_template(template_id: str) -> Template:
    print("template_id",template_id)
    template = templates_collection.find_one({"_id": ObjectId(template_id)})
    print("template",template)
    if template:
        return Template(id=str(template['_id']),**template)
    else:
        raise HTTPException(status_code=404, detail="Template not found")

def update_template(template_id: str, template_data: TemplateUpdate) -> Template:
    template_dict = template_data.dict()
    result = templates_collection.update_one(
        {"_id": ObjectId(template_id)},
        {"$set": template_dict}
    )
    if result.modified_count == 1:
        return {**template_data.dict(), "id": template_id}
    else:
        raise HTTPException(status_code=404, detail="Template not found")

def delete_template(template_id: str):
    result = templates_collection.delete_one({"_id": ObjectId(template_id)})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail="Template not found")
