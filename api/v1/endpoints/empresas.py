# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union
from sqlalchemy import update, text, delete
from main import db_dependency

from models.db_models import EmpresasDB, VendeEmDB, MarketplacesDB
from models.schemas import empresas, vende_em

router = APIRouter(prefix="/empresas", tags=["Empresas"])

@router.get('/')
async def get_empresas(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> empresas.EmpresaListingResponse:
    stmt = db.query(EmpresasDB)
    empresas_data = stmt.order_by(EmpresasDB.id_empresa.asc()).limit(limit).offset(offset)
    return {
        'empresas': empresas_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}} 

@router.post('/')
async def insert_empresas(
    empresas: Union[empresas.EmpresaCreate, List[empresas.EmpresaCreate]],
    db: db_dependency = None
):
    if isinstance(empresas, list):
        for empresa in empresas:
            empresa_db = EmpresasDB(**empresa.model_dump())
            db.add(empresa_db)
    else:
        empresa_db = EmpresasDB(**empresas.model_dump())
        db.add(empresa_db)
    db.commit()
    return {"msg": "Empresa(s) inserida(s) com sucesso!"}

@router.patch('/')
async def update_empresa(
    id_empresa: Annotated[int, Query(description="Id da empresa que será alterada")],
    empresa: empresas.EmpresaPatch,
    db: db_dependency
):
    stmt = update(EmpresasDB).where(EmpresasDB.id_empresa == id_empresa).values(**empresa.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()

@router.delete('/')
async def delete_empresa(
    id_empresa: Annotated[int, Query(description="Id da empresa que será deletada")],
    db: db_dependency
): 
    stmt = delete(EmpresasDB).where(EmpresasDB.id_empresa == id_empresa)
    db.execute(stmt)
    db.commit()
    
@router.get('/marketplaces')
async def get_empresa_marketplace(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
) -> vende_em.EmpresaMarketplaceResponse|List[vende_em.EmpresaMarketplaceResponse]:
    empresas = db.query(EmpresasDB).all()
    
    stmt = text('\
        SELECT m.*\
        FROM empresas e\
        JOIN "vendeEm" ve ON ve.id_empresa = e.id_empresa\
        JOIN marketplaces m ON m.id_marketplace = ve.id_marketplace\
        WHERE e.id_empresa = :id_empresa;\
        ')
    
    marketplaces_list: List[vende_em.EmpresaMarketplaceResponse] = []
    
    for empresa in empresas:
        marketplaces_list.append(
            vende_em.EmpresaMarketplaceResponse(
                **empresa.__dict__, 
                marketplaces=db.execute(stmt, {"id_empresa": empresa.id_empresa}).mappings().all()
                )
            )
        
    return marketplaces_list
    
    
@router.post('/marketplaces')
async def insert_empresa_marketplace(
    vende_em: Union[vende_em.VendeEmCreate, List[vende_em.VendeEmCreate]],
    db: db_dependency
):
    if isinstance(vende_em, list):
        for listagem in vende_em:
            vende_em_db = VendeEmDB(**listagem.model_dump())
            db.add(vende_em_db)
    else:
        vende_em_db = VendeEmDB(**vende_em.model_dump())
        db.add(vende_em_db)
    db.commit()