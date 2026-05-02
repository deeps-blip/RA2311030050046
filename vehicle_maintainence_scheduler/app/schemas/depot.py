from pydantic import BaseModel

class Depot(BaseModel):
    id: str
    mechanic_hours: int
