from pydantic import BaseModel, ConfigDict, Field

COLOR_PATTERN = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

class CategoriesBase(BaseModel):
    pass

class ProjectsInCategory(BaseModel):
    id: int
    name: str = Field(
        max_length=50
    )
    label: str

class CategoriesByUserResponse(CategoriesBase):
    id: int
    name: str
    color: str = Field(
        pattern=COLOR_PATTERN
    )
    description: str

    projects: list[ProjectsInCategory]

    model_config= ConfigDict(from_attributes=True)

class CreateCategoryRequest(CategoriesBase):
    name: str
    color: str = Field(
        pattern=COLOR_PATTERN
    )
    description: str

class CreateCategoryResponse(CreateCategoryRequest):
    id: int    

class GetCategoryResponse(CategoriesBase):
    id: int
    name: str
    color: str = Field(
        pattern=COLOR_PATTERN
    )
    description: str

class UpdateCategoryRequest(CategoriesBase):
    name: str | None = None
    color: str | None = Field(
        pattern=COLOR_PATTERN,
        default=None
    )
    description: str | None = None

class UpdateCategoryResponse(UpdateCategoryRequest):
    pass