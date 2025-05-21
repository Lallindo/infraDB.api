from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase

class EmpresaBase(BaseModel):
    descritivo_empresa: str = Field(default="nome", description="Nome da empresa")

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaResponse(EmpresaBase):
    id_empresa: int = Field(description="Id da empresa")

class EmpresaPatch(EmpresaCreate):
    pass

class EmpresaListingResponse(BaseModel):
    empresas: List[EmpresaResponse]
    paginacao: ResponseBase