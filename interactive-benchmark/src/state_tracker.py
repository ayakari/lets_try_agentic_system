from state_schema import CanonicalState


class StateTracker:
    def __init__(self):
        self.state = CanonicalState()

    def get_state(self) -> CanonicalState:
        return self.state

    def apply_changes(self, changes: list[str]) -> None:
        # TODO: implement structured state updates
        pass
