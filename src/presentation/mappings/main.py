from datetime import datetime

from adaptix import P, Retort, dumper, validator
from adaptix.conversion import allow_unlinked_optional

from src.infrastructure.database.models.movie import Actor, Movie

data_mapper = Retort(
    recipe=[
        dumper(datetime, lambda x: x.date()),
    ]
)


actor_mapper = data_mapper.extend(
    recipe=[
        validator(
            P[Actor].birth_day,
            lambda x: x <= datetime.now().date(),
            "Birth day may be before today",
        ),
        validator(
            P[Actor].first_name,
            lambda x: len(x) >= 10,
            "Incorrect",
        ),
    ]
)


movie_mapper = data_mapper.extend(recipe=[allow_unlinked_optional(P[Movie].slug)])
