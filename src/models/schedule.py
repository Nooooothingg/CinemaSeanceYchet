from dataclasses import dataclass
import datetime
@dataclass
class Schedule:
    schedule_id: int
    date_time: datetime.datetime
    film_id: int
    cinema_id: int
    admin_id: int

    film_name: str | None = None
    cinema_name: str | None = None
    film_time: int | None = None
    cinema_link: str | None = None

