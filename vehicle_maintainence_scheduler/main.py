from fastapi import FastAPI
from pydantic import BaseModel


mechanicsdict = {}

vehiclesdict = {}

app = FastAPI()

class Depot(BaseModel):
    name: str
    location: str

class Vehicle(BaseModel):
    taskID: str
    Duration: int
    Impact: int

@app.post("/add_mechanic/")
def add_mechanic(mechanic: Mechanic):
    mechanicsdict[mechanic.name] = mechanic
    return {"message": "Mechanic added successfully"}