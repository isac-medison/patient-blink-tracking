from uuid import UUID

class EntityNotFoundError(Exception):
    def __init__(self, entity_id: UUID):
        self.entity_id = entity_id

    def __str__(self) -> str:
        return f"Entity not found: {self.entity_id}"
