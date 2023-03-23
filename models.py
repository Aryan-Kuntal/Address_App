from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Address_model(BaseModel):
    latitude : float
    longitude : float

class update_Address_model(BaseModel):
    id : int
    latitude : Optional[float]
    longitude : Optional[float]