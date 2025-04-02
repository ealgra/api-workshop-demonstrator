from item_service import ItemService
from items import Item, ItemPatch
from typing_extensions import Annotated, Union, List
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, Response, Query, Header
from fastapi.responses import JSONResponse, PlainTextResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class ItemFilterParams(BaseModel):
     name: str = None
     min_price: int = Field(None, ge=0)
     max_price: int = Field(None, ge=0)

@app.get("/items")
def get_items(req: Request, q: Annotated[ItemFilterParams, Query()]) -> Union[List[Item], None]:
        items = ItemService.query_items(q.name, q.min_price, q.max_price)
        return items


@app.get("/items/{item_id}")
def read_item(item_id: int, re: Response, if_not_match: Annotated[Union[str, None], Header()] = None) -> Item:
        item = ItemService.read_item(item_id)
        
        if item is None: 
            return PlainTextResponse(status_code=404, content="Item not found")
        
        if if_not_match is not None and (item.hash() == if_not_match):
             return PlainTextResponse(status_code=304, content="Item not modified")
        
        re.headers.append("ETag", item.hash())
        return item

@app.put("/items/{item_id}")
def put_item(item: Item, item_id: int, re: Response, if_match: Annotated[Union[str, None], Header()] = None) -> Item:
        existing = ItemService.read_item(item_id)
        if existing is None: 
            return PlainTextResponse(status_code=404, content="Item not found")
        
        if if_match is not None and (existing.hash() != if_match):
             return PlainTextResponse(status_code=412, content="Item was modified by someone else")
        
        updated = ItemService.update_item(item)

        re.headers.append("ETag", updated.hash())
        return updated

@app.post("/items")
def create_item(item: Item) -> Item:
    created = ItemService.add_item(item)
    if created is None:
       return Response(status_code=400)
    
    headers = {}
    headers["ETag"] = created.hash()
    headers["Location"] = f"/items/{created.id}"
    return JSONResponse(status_code=201, content=dict(created), headers=headers)

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
     deleted = ItemService.delete_item(item_id)
     if not deleted:
          return PlainTextResponse(status_code=404, content="Item not found")
     return


@app.get("/items/{item_id}/is_available")
def read_item(item_id: int, re: Response, if_not_match: Annotated[Union[str, None], Header()] = None) -> bool:
        item = ItemService.read_item(item_id)
        
        if item is None: 
            return PlainTextResponse(status_code=404, content="Item not found")
        return item.is_available

@app.patch("/items/{item_id}")
def patch_item(itempatch: ItemPatch, item_id: int, re: Response, if_match: Annotated[Union[str, None], Header()] = None) -> Item:
        existing = ItemService.read_item(item_id)
        if existing is None: 
            return PlainTextResponse(status_code=404, content="Item not found")
        
        if if_match is not None and (existing.hash() != if_match):
             return PlainTextResponse(status_code=412, content="Item was modified by someone else")
        
        updated = ItemService.patch_item(item_id, itempatch)

        re.headers.append("ETag", updated.hash())
        return updated
