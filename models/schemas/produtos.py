from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase

class ProdutoBase(BaseModel):
    id_tiny_prod: str = Field(default="id tiny", description="Id do produto no Tiny")
    descritivo_prod: str = Field(default="nome", description="Nome do produto") 
    sku_prod: str = Field(default="sku", description="SKU do produto")
    gtin_prod: str = Field(default="gtin", description="GTIN/EAN do produto")
    preco_prod: float = Field(default=-1, description="Preço de venda do produto")
    custo_prod: float = Field(default=-1, description="Preço de custo do produto")
    tipo_prod: str = Field(default="tipo", description="Tipo do produto, deve ser 'kit', 'simples' ou 'outro'")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id_prod: int = Field(description="Id do produto")
    
class ProdutoMarcaResponse(ProdutoResponse):
    marca_prod: Optional[str] = Field(description="Nome da marca do produto")
    
class ProdutoCategoriaResponse(ProdutoResponse):
    categoria_prod: Optional[str] = Field(description="Nome da categoria do produto")
    
class ProdutoEmpresasResponse(BaseModel):
    empresa: Optional[str] = Field(description="Lista com todas as empresas que vendem o produto")
    
class ProdutoMarketplacesResponse(BaseModel):
    marketplace: Optional[str] = Field(description="Lista com todos os marketplaces onde o produto está listado")
    
class ProdutoEmpresaMarketResponse(ProdutoMarketplacesResponse, ProdutoEmpresasResponse):
    codigo_marketplace: str = Field(description="Código do produto no marketplace")
    preco_marketplace: float = Field(description="Preço do produto no marketplace")
    
class ProdutoListagens(ProdutoResponse):
    listagens: List[ProdutoEmpresaMarketResponse]
    
class ProdutoFullResponse(ProdutoMarcaResponse, ProdutoCategoriaResponse, ProdutoResponse):
    pass
    
class ProdutoPatch(ProdutoCreate):
    estoque_prod: Optional[int] = Field(default=None ,example=None, examples=[None])
    marca_prod: Optional[int] = Field(default=None ,example=None, examples=[None])
    categoria_prod: Optional[int] = Field(default=None ,example=None, examples=[None])

class ProdutoBaseListing(BaseModel):
    produtos: List[ProdutoResponse]
    paginacao: ResponseBase

class ProdutoFullListingResponse(BaseModel):
    produtos: List[ProdutoFullResponse]
    paginacao: ResponseBase