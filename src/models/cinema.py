from dataclasses import dataclass

@dataclass
class Cinema:
    cinema_id: int
    cinemaname: str
    description: str | None = None
    link: str | None = None