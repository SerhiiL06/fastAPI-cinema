from adaptix import P
from adaptix.conversion import allow_unlinked_optional, coercer, get_converter

from src.infrastructure.database.models.movie import Actor, Movie

from .actor import CreateActorDto
from .movie import MovieDto

dto_to_actor = get_converter(
    CreateActorDto,
    Actor,
    recipe=[
        allow_unlinked_optional(P[Actor].movies, P[Actor].country, P[Actor].id),
        coercer(str, str, lambda x: x.lower()),
    ],
)
