from dataclasses import dataclass

@dataclass
class Film:
    film_id: int
    film_name: str
    film_time: int
    film_descr: str | None = None