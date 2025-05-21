from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase
from .produtos import ProdutoResponse

class ProdutoVarResponse(BaseModel):
    id_prod: int = Field(description="Id do produto pai")
    descritivo_prod: str = Field(description="Nome do produto pai")
    
class ProdutoPaiVarResponse(ProdutoVarResponse):
    variacoes: List[ProdutoResponse]
    
class ProdutoFilhoVarResponse(ProdutoVarResponse):
    e_variacao_de: List[ProdutoResponse]