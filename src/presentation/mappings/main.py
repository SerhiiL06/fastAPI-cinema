from datetime import datetime

from adaptix import P, Retort, dumper, validator

from src.infrastructure.database.models.movie import Actor

data_mapper = Retort(
    recipe=[
        dumper(datetime, lambda x: x.date()),
        validator(
            P[Actor].birth_day,
            lambda x: x <= datetime.now().date(),
            "Birth day may be before today",
        ),
    ]
)
