from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase

class KitBase(BaseModel):
    id_prod_pai: int = Field(description="Id do produto kit")
    id_prod_filho: int = Field(description="Id do produto que compõe o kit")
    quant_por_kit: int = Field(description="Quantidade do produto filho no kit", default=None, example=None, examples=[None])

class KitCreate(KitBase):
    pass

class KitResponse(KitBase):
    id_kit: int = Field(description="Id do kit")

class KitPatch(BaseModel):
    quant_por_kit: Optional[int] = Field(description="Quantidade do produto filho no kit", default=None, example=None, examples=[None])

class KitListingResponse(BaseModel):
    kits: List[KitResponse]
    paginacao: ResponseBase 
    