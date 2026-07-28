from datetime import date

from pydantic import BaseModel, ConfigDict

from app.core.enums import Priorities


class TasksBase(BaseModel):
    pass

class CreateTaskRequest(TasksBase):
    deadline: date
    label: str
    description: str
    priority: Priorities
    project_id: int

class CreateTaskResponse(CreateTaskRequest):
    id: int
    owner_id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


class GetTasksByProjectResponse(BaseModel):
    deadline: date
    label: str
    description: str
    priority: Priorities
    id: int
    owner_id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)

class UpdateTask(BaseModel):
    deadline: date | None = None
    label: str | None = None
    description: str | None = None
    priority: Priorities | None = None
    project_id: int