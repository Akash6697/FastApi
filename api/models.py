from pydantic import BaseModel

class TemplateCreate(BaseModel):
    template_name: str
    subject: str
    body: str
    id: str
    
class NewTemplateCreate(BaseModel):
    template_name: str
    subject: str
    body: str

class TemplateUpdate(BaseModel):
    template_name: str
    subject: str
    body: str

class Template(TemplateCreate):
    _id: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
