import typing as tp

from pydantic import BaseModel, ConfigDict, Field

PERFECT_CONFIG = ConfigDict(
    frozen=True,
    strict=True,
    serialize_by_alias=True,
)

class Test(BaseModel):
    model_config = PERFECT_CONFIG

    x: tp.Iterable[int]

a = Test(x=[1, 2, 3])
print(a)
print(a.x)
print([*a.x])
b = Test.model_validate_json(
    '{"x": [1, 2, 3]}'
)
print(b)
print(b.x)
print([*b.x])

import pdb; pdb.set_trace()

# nb
