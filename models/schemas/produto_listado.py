from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase
from .produtos import ProdutoResponse
from .empresas import EmpresaResponse
from .marketplaces import MarketplaceResponse

class ProdutoListadoBase(BaseModel):
    id_produto: int = Field(default=-1, description="Id do produto listado")
    id_vende_em: int = Field(default=-1, description="Id da relação entre empresa e marketplace da listagem")
    codigo_marketplace: str = Field(default="codigo", description="Código do produto dentro do marketplace")
    preco_marketplace: float = Field(default=-1, description="Preço do produto no marketplace")

class ProdutoListadoCreate(ProdutoListadoBase):
    pass

class ProdutoListadoResponse(ProdutoListadoBase):
    id_produto_listado: int = Field(description="Id da listagem")

class ProdutoListadoPatch(ProdutoListadoCreate):
    pass

class ProdutoListadoListingResponse(BaseModel):
    produtos_listados: List[ProdutoListadoResponse]
    paginacao: ResponseBase

    