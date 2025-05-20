# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union
from sqlalchemy import update, text, delete
from app.main import db_dependency

from models.db_models import MarketplacesDB, VendeEmDB
from models.schemas import marketplaces, vende_em

router = APIRouter(prefix="/marketplaces", tags=["Marketplaces"])

@router.get('/')
async def get_marketplaces(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> marketplaces.MarketplaceListingResponse:
    stmt = db.query(MarketplacesDB)
    marketplaces_data = stmt.order_by(MarketplacesDB.id_marketplace.asc()).limit(limit).offset(offset)
    return {
        'marketplaces': marketplaces_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}} 

@router.post('/')
async def insert_marketplaces(
    marketplaces: Union[marketplaces.MarketplaceCreate, List[marketplaces.MarketplaceCreate]],
    db: db_dependency = None
):
    if isinstance(marketplaces, list):
        for marketplace in marketplaces:
            marketplace_db = MarketplacesDB(**marketplace.model_dump())
            db.add(marketplace_db)
    else:
        marketplace_db = MarketplacesDB(**marketplaces.model_dump())
        db.add(marketplace_db)
    db.commit()
    return {"msg": "Marketplace(s) inserido(s) com sucesso!"}

@router.patch('/')
async def update_marketplaces(
    id_marketplace: Annotated[int, Query(description="Id do marketplace que será alterada")],
    marketplace: marketplaces.MarketplacePatch,
    db: db_dependency
):
    stmt = update(MarketplacesDB).where(MarketplacesDB.id_marketplace == id_marketplace).values(**marketplace.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()

@router.delete('/')
async def delete_empresa(
    id_marketplace: Annotated[int, Query(description="Id do marketplace que será deletada")],
    db: db_dependency
): 
    stmt = delete(MarketplacesDB).where(MarketplacesDB.id_marketplace == id_marketplace)
    db.execute(stmt)
    db.commit()
    
@router.get('/empresas')
async def get_marketplace_empresa(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
) -> vende_em.MarketplaceEmpresaResponse|List[vende_em.MarketplaceEmpresaResponse]:
    marketplaces = db.query(MarketplacesDB).all()
    
    stmt = text('\
        SELECT e.*\
        FROM marketplaces m\
        JOIN "vendeEm" ve ON ve.id_marketplace = m.id_marketplace\
        JOIN empresas e ON e.id_empresa = ve.id_empresa\
        WHERE m.id_marketplace = :id_marketplace;\
        ')
    
    empresas_list: List[vende_em.EmpresaMarketplaceResponse] = []
    
    for marketplace in marketplaces:
        empresas_list.append(
            vende_em.MarketplaceEmpresaResponse(
                **marketplace.__dict__, 
                empresas=db.execute(stmt, {"id_marketplace": marketplace.id_marketplace}).mappings().all()
                )
            )
        
    return empresas_list