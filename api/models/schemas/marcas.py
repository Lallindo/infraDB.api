from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase
from .produtos import ProdutoBaseListing

class MarcaBase(BaseModel):
    descritivo_marca: str = Field(default="nome" ,description="Nome da marca")

class MarcaCreate(MarcaBase):
    pass

class MarcaResponse(MarcaBase):
    id_marca: int = Field(description="Id da marca")
    
class MarcaProdutosResponse(ProdutoBaseListing, MarcaResponse):
    pass

class MarcaPatch(MarcaCreate):
    pass
    
class MarcaListingResponse(BaseModel):
    marcas: List[MarcaResponse]
    paginacao: ResponseBase