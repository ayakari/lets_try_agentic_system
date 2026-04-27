from pydantic import BaseModel, Field
from typing import List


class EventRecord(BaseModel):
    turn_id: int
    user_action: str = ""
    system_action: str = ""
    state_changes: List[str] = Field(default_factory=list)
    new_facts: List[str] = Field(default_factory=list)
    updated_facts: List[str] = Field(default_factory=list)
    opened_loops: List[str] = Field(default_factory=list)
    resolved_loops: List[str] = Field(default_factory=list)
