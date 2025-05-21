from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase

class VariacaoBase(BaseModel):
    id_prod_pai: int = Field(description="Id do produto pai da variação")
    id_prod_filho: int = Field(description="Id do produto filho da variação")

class VariacaoCreate(VariacaoBase):
    pass

class VariacaoResponse(VariacaoBase):
    id_variacao: int = Field(description="Id da variação")

class VariacaoListingResponse(BaseModel):
    variacoes: List[VariacaoResponse]
    paginacao: ResponseBase