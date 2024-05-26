from datetime import datetime

from adaptix import Retort, dumper

data_mapper = Retort(recipe=[dumper(datetime, lambda x: x.date())])
