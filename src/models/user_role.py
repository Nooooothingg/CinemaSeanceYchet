from dataclasses import dataclass

@dataclass
class UserRole:
    role_id: int
    role_name: str
    description: str | None = None