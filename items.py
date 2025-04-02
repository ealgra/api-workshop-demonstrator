from typing import Union
from pydantic import BaseModel
import json

class Item(BaseModel):
    id: int = None
    name: str
    price: float
    is_offer: Union[bool, None] = None
    is_available: Union[bool, None] = True

    def hash(self)->str:
        return str(hash(json.dumps(self.dict(), sort_keys=True)))


class ItemPatch(BaseModel):
    price: Union[float, None] = None
    is_offer: Union[bool, None] = None
    is_available: Union[bool, None] = None