from pydantic import BaseModel, ConfigDict


class ConceptResponse(BaseModel):
    id: int
    name: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    id: int
    concept_id: int
    title: str
    type: str
    difficulty: str
    description: str
    template_code: str
    hint_text: str | None
    model_config = ConfigDict(from_attributes=True)
