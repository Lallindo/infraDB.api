from pydantic import BaseModel, Field
from typing import List
from .produtos import ProdutoResponse

class KitFullResponse(BaseModel):
    id_kit: int = Field(description="Id do kit")
    prod_pai: ProdutoResponse = Field(description="Produto kit")
    prod_filho: ProdutoResponse = Field(description="Produto composição")
    quant_por_kit: int = Field(description="Quantidade de produtos composição em um kit")
    
class ProdutoKitResponse(BaseModel):
    id_prod: int = Field(description="Id do produto")
    descritivo_prod: str = Field(description="Nome do produto")
    kit_contem: List["ProdutoForKitResponse"] = Field(description="Composições contidas pelo kit")
    
class ProdutoComposicaoResponse(BaseModel):
    id_prod: int = Field(description="Id do produto")
    descritivo_prod: str = Field(description="Nome do produto")
    faz_parte_de: List["ProdutoForKitResponse"] = Field(description="Lista de kits que o produto faz parte")
    
class ProdutoForKitResponse(ProdutoResponse):
    quant_por_kit: int = Field(description="Quantidade de produtos composição em um kit")