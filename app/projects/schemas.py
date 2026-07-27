from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel): 
    name: str
    description: str
    label: str

class ProjectResponse(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProjectCreateRequest(ProjectBase):
    category_id: int

class ProjectCreateResponse(ProjectCreateRequest):
    id: int

class ProjectUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    label: str | None = None

class ProjectUpdateResponse(ProjectUpdateRequest):
    pass 

