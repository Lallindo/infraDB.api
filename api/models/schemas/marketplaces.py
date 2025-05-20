from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from .response import ResponseBase

class MarketplaceBase(BaseModel):
    descritivo_marketplace: str = Field(default="nome", description="Nome do marketplace")

class MarketplaceCreate(MarketplaceBase):
    pass

class MarketplaceResponse(MarketplaceBase):
    id_marketplace: int = Field(description="Id do marketplace")

class MarketplacePatch(MarketplaceCreate):
    pass

class MarketplaceListingResponse(BaseModel):
    marketplaces: List[MarketplaceResponse]
    paginacao: ResponseBase