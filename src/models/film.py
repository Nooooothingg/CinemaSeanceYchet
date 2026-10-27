from dataclasses import dataclass

@dataclass
class Film:
    film_id: int
    film_name: str
    film_descr: str | None = None
    film_time: int