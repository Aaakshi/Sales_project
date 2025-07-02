from pydantic import BaseModel

class RegionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True