from datetime import date

from pydantic import BaseModel

from app.core.enums import Priorities


class SubtaskBase(BaseModel):
    pass

class CreateSubtaskRequest(SubtaskBase):
    deadline: date
    label: str
    description: str
    priority: Priorities



class CreateSubtaskResponse(CreateSubtaskRequest):
    id: int

class GetSubtasksResponse(SubtaskBase):
    id: int
    deadline: date
    description: str
    priority: Priorities

class UpdateSubtaskRequest(SubtaskBase):
    deadline: date | None = None
    label: str | None = None
    description: str | None = None
    priority: Priorities | None = None

class UpdateSubtaskResponse(UpdateSubtaskRequest):
    pass