from datetime import datetime
from src.infrastructure.database.models.movie import Actor
from adaptix import Retort, dumper, validator, P

data_mapper = Retort(
    recipe=[
        dumper(datetime, lambda x: x.date()),
        validator(
            P[Actor].birth_day,
            lambda x: x >= datetime.now().date(),
            "Birth day may be before today",
        ),
    ]
)
