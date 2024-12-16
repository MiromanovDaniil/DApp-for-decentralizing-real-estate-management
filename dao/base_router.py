from hashlib import sha256

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.post("/create")
async def create_smart_contract():
    pass


@app.post("/sign")
async def sign_smart_contract():
    pass


@app.post("/got")
async def get_smart_contract():
    pass


@app.post("/cancel")
async def cancel_smart_contract():
    pass
