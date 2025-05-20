from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase
from .empresas import EmpresaResponse
from .marketplaces import MarketplaceResponse

class VendeEmBase(BaseModel):
    id_empresa: int = Field(default=-1, description="Id da empresa")
    id_marketplace: int = Field(default=-1, description="Id do marketplace")

class VendeEmCreate(VendeEmBase):
    pass

class VendeEmResponse(VendeEmBase):
    id_vende_em: int = Field(description="Id da relação de em qual marketplace uma empresa vende")

class VendeEmPatch(VendeEmCreate):
    pass

class VendeEmListingResponse(BaseModel):
    vende_em_results: List[VendeEmResponse]
    paginacao: ResponseBase
    
class EmpresaMarketplaceResponse(EmpresaResponse):
    marketplaces: List[MarketplaceResponse]
    
class MarketplaceEmpresaResponse(MarketplaceResponse):
    empresas: List[EmpresaResponse]