from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    userrole_id: int
    username: str
    login: str
    passwordhash: str