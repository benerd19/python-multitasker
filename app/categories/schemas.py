from pydantic import BaseModel, ConfigDict


class CategoriesBase(BaseModel):
    pass

class ProjectsInCategory(BaseModel):
    id: int
    name: str
    label: str

class CategoriesByUserResponse(CategoriesBase):
    id: int
    name: str
    color: str
    description: str

    projects: list[ProjectsInCategory]

    model_config= ConfigDict(from_attributes=True)

class CreateCategoryRequest(CategoriesBase):
    name: str
    color: str
    description: str

class CreateCategoryResponse(CreateCategoryRequest):
    id: int    

class GetCategoryResponse(CategoriesBase):
    id: int
    name: str
    color: str
    description: str

class UpdateCategoryRequest(CategoriesBase):
    name: str | None = None
    color: str | None = None
    description: str | None = None

class UpdateCategoryResponse(UpdateCategoryRequest):
    pass