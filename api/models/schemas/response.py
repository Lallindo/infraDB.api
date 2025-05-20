from pydantic import BaseModel

class ResponseBase(BaseModel):
    offset: int
    limit: int
    total: int