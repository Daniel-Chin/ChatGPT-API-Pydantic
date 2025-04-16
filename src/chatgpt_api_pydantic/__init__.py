import typing as tp
from functools import lru_cache, wraps

from pydantic import BaseModel, ConfigDict, Field

PERFECT_CONFIG = ConfigDict(
    frozen=True,
    strict=True,
    serialize_by_alias=True,
)

SomeBaseModel = tp.TypeVar("SomeBaseModel", bound=tp.Type[BaseModel])
def autoCache(cls: SomeBaseModel) -> SomeBaseModel:
    assert cls.model_config.get('frozen', False), "autoCache can only be used with frozen models"
    cls.model_validate_json = wraps(cls.model_validate_json)(
        lru_cache(maxsize=None)(cls.model_validate_json), 
    )
    cls.model_dump_json = wraps(cls.model_dump_json)(
        lru_cache(maxsize=None)(cls.model_dump_json),
    )   # type: ignore[assignment]
    # frozen models are hashable, but that's hard to statically infer
    return cls

@autoCache
class FunctionTool(BaseModel):
    model_config = PERFECT_CONFIG

    class Parameters(BaseModel):
        model_config = PERFECT_CONFIG

        class Property(BaseModel):
            model_config = PERFECT_CONFIG

            type_: str = Field(alias='type')
            description: str
        
        type_: str = Field(alias='type')
        properties: tp.Dict[str, Property]
        required: tp.List[str]
        additionalProperties: bool
    
    type_: str = Field(alias='type')
    name: str
    description: str
    parameters: Parameters
    strict: bool | None

    @classmethod
    def new(
        cls, 
        name: str, 
        description: str,
        parameters: tp.Iterable[tp.Tuple[
            str, # name
            str, # type
            str, # description
            bool, # is_required
        ]], 
        strict: bool | None = False,
    ):
        '''
        A more readable constructor
        '''
        properties = {}
        required = []
        for name, type_, description, is_required in parameters:
            properties[name] = cls.Parameters.Property(
                type=type_,
                description=description,
            )
            if is_required:
                required.append(name)
        return cls(
            type='function',
            name=name,
            description=description,
            parameters=cls.Parameters(
                type='object',
                properties=properties,
                required=required,
                additionalProperties=False,
            ),
            strict=strict, 
        )

@autoCache
class FunctionToolCall(BaseModel):
    model_config = PERFECT_CONFIG

    class Function(BaseModel):
        model_config = PERFECT_CONFIG

        name: str
        arguments: str

    id_: str = Field(alias='id')
    type_: str = Field(alias='type')
    function: Function
