# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union
from sqlalchemy import update, text, delete
from main import db_dependency

from models.db_models import KitsDB
from models.schemas import kits, em_kit

router = APIRouter(prefix="/kits", tags=["Kits"])

@router.get('/')
async def get_kits(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> kits.KitListingResponse:
    stmt = db.query(KitsDB)
    kits_data = stmt.order_by(KitsDB.id_kit.asc()).limit(limit).offset(offset)
    return {
        'kits': kits_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}}

@router.post('/') # TODO Checar se o produto filho é "simples", caso não seja, inserção deve ser negada
async def insert_kits(
    kits: Union[kits.KitCreate, List[kits.KitCreate]],
    db: db_dependency = None
):
    if isinstance(kits, list):
        for kit in kits:
            kit_db = KitsDB(**kit.model_dump())
            db.add(kit_db)
    else:
        kit_db = KitsDB(**kits.model_dump())
        db.add(kit_db)
    db.commit()
    return {"msg": "kit(s) inserido(s) com sucesso!"}

@router.patch('/')
async def update_kit(
    id_kit: Annotated[int, Query(description="Id do kit que será alterado")],
    kit: kits.KitPatch,
    db: db_dependency
): 
    stmt = update(KitsDB).where(KitsDB.id_kit == id_kit).values(**kit.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()
    
@router.delete('/')
async def delete_kit(
    id_kit: Annotated[int, Query(description="Id do kit que será deletado")],
    db: db_dependency
): 
    stmt = delete(KitsDB).where(KitsDB.id_kit == id_kit)
    db.execute(stmt)
    db.commit()