from dataclasses import dataclass
import datetime
@dataclass
class Schedule:
    schedule_id: int
    date_time: datetime.datetime
    film_name: str
    cinema_id: int
    admin_id: int

