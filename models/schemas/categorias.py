from pydantic import BaseModel, Field
from typing import List
from .response import ResponseBase
from .produtos import ProdutoBaseListing

class CategoriaBase(BaseModel):
    descritivo_categoria: str = Field(default="nome", description="Nome da categoria")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id_categoria: int = Field(description="Id da categoria")

class CategoriaProdutosResponse(ProdutoBaseListing, CategoriaResponse):
    pass

class CategoriaPatch(CategoriaCreate):
    pass

class CategoriaListingResponse(BaseModel):
    categorias: List[CategoriaResponse]
    paginacao: ResponseBase