from humps import camelize
from pydantic import BaseModel, ConfigDict


def to_camel(string):
    return camelize(string)


class CamelMode(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )
