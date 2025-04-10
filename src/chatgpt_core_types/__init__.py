import typing as tp
from dataclasses import dataclass
from functools import lru_cache

@dataclass(frozen=True)
class Property:
    name: str
    type_: str
    description: str
    is_required: bool

@dataclass(frozen=True)
class FunctionTool:
    name: str
    description: str
    parameters: tp.Iterable[Property]
    strict: bool | None = False

    @lru_cache(maxsize=None)
    def toPrimitive(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    p.name: {
                        "type": p.type_,
                        "description": p.description,
                    } for p in self.parameters
                },
                "required": [
                    p.name for p in self.parameters if p.is_required
                ],
                "additionalProperties": False, 
            },
            "strict": self.strict,
        }
