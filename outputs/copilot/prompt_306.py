from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    value: int


@app.get("/status")
def read_status():
    return {"status": "ok"}


@app.post("/process")
def process_item(item: Item):
    result = item.value * 2
    return {"name": item.name, "original_value": item.value, "processed_value": result}

