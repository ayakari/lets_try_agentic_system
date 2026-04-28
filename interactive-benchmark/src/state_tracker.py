from copy import deepcopy

from rules.scene_rules import apply_scene_rules
from rules.reaction_rules import apply_reaction_rules
from rules.memory_rules import apply_memory_rules


class StateTracker:
    def __init__(self, initial_state: dict):
        self.state = deepcopy(initial_state)

    def get_state(self) -> dict:
        return deepcopy(self.state)

    def apply_user_action(self, user_action: str) -> dict:
        text = (user_action or "").lower()

        apply_scene_rules(self.state, text)
        apply_reaction_rules(self.state, text)
        apply_memory_rules(self.state, text)

        return self.get_state()
