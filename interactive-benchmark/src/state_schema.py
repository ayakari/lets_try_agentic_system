from pydantic import BaseModel, Field
from typing import List, Dict


class SceneState(BaseModel):
    phase: str = ""
    location: str = ""
    distance: str = ""
    recent_events: List[str] = Field(default_factory=list)


class CharacterState(BaseModel):
    intent: str = ""
    emotion: str = ""
    initiative: float = 0.0


class MemoryState(BaseModel):
    stable_facts: List[str] = Field(default_factory=list)
    recent_facts: List[str] = Field(default_factory=list)
    updated_facts: List[str] = Field(default_factory=list)


class TensionState(BaseModel):
    open_loops: List[str] = Field(default_factory=list)
    pace: float = 0.0
    novelty_budget: float = 0.0


class CanonicalState(BaseModel):
    scene: SceneState = SceneState()
    characters: Dict[str, CharacterState] = Field(default_factory=lambda: {
        "user_side": CharacterState(),
        "other_side": CharacterState()
    })
    memory: MemoryState = MemoryState()
    tension: TensionState = TensionState()
