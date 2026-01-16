from typing import List, Optional, Type
from pydantic import BaseModel, create_model
from pydantic.config import ConfigDict

def generate_partial_model(base_model: Type[BaseModel],required_attr:List = [], model_name: str = "PartialModel") -> Type[BaseModel]:
    fields = {
        name: (Optional[field], None)
        if name not in required_attr else (field, ...)
        for name, field in base_model.__annotations__.items()
    }

    # Preserve config if available
    config = getattr(base_model, 'model_config', ConfigDict())

    return create_model(
        model_name,
        __base__=base_model,
        __config__=config,
        **fields
    )