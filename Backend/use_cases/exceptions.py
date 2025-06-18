from uuid import UUID

class EntityNotFoundError(Exception):
    def __init__(self, entity_id: int):
        self.entity_id = entity_id

    def __str__(self) -> str:
        return f"Entity not found: id == {self.entity_id}"

class ExternalError(Exception):
    pass

class DatabaseError(ExternalError):
    def __init__(self, error: Exception):
        self.error = error

    def __str__(self) -> str:
        return str(self.error)
