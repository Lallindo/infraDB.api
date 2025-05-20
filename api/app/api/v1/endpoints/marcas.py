# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union, Optional
from sqlalchemy import update, text, delete
from app.main import db_dependency

from models.db_models import MarcasDB, ProdutosDB
from models.schemas import marcas

router = APIRouter(prefix="/marcas", tags=["Marcas"])

@router.get('/')
async def get_marcas(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> marcas.MarcaListingResponse:
    stmt = db.query(MarcasDB)
    marca_data = stmt.order_by(MarcasDB.id_marca.asc()).limit(limit).offset(offset)
    return {
        'marcas': marca_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}} 

@router.post('/')
async def insert_marcas(
    marcas: Union[marcas.MarcaCreate, List[marcas.MarcaCreate]],
    db: db_dependency = None
):
    if isinstance(marcas, list):
        for marca in marcas:
            marca_db = MarcasDB(**marca.model_dump())
            db.add(marca_db)
    else:
        marca_db = MarcasDB(**marcas.model_dump())
        db.add(marca_db)
    db.commit()
    return {"msg": "Marcas(s) inserida(s) com sucesso!"}

@router.patch('/')
async def update_marca(
    id_marca: Annotated[int, Query(description="Id da marca que será alterada")],
    marca: marcas.MarcaPatch,
    db: db_dependency
): 
    stmt = update(MarcasDB).where(MarcasDB.id_marca == id_marca).values(**marca.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()
    
@router.delete('/')
async def delete_marca(
    id_marca: Annotated[int, Query(description="Id da marca que será deletado")],
    db: db_dependency
): 
    stmt = delete(MarcasDB).where(MarcasDB.id_marca == id_marca)
    db.execute(stmt)
    db.commit()

@router.get('/produtos', description="Busca todos os produtos relacionados com uma marca. Caso Id e Nome sejam fornecidos, Id será priorizado.")
async def get_produtos_marcas(
    id_marca: Annotated[Optional[int], Query(description="Id da marca")] = None,
    nome_marca: Annotated[Optional[str], Query(description="Nome da marca")] = None,
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
):
    if id_marca is not None:
        marca = db.get(MarcasDB, id_marca)
    elif nome_marca is not None:
        marca = db.query(MarcasDB).where(MarcasDB.descritivo_marca.contains(nome_marca)).first()
    else:
        return {"msg": "Envie Id ou Nome para buscar"}
        
    stmt = text("\
        SELECT p.*\
        FROM marcas m\
        JOIN produtos p ON p.marca_prod = m.id_marca\
        WHERE m.id_marca = :id_marca\
        LIMIT :limit\
        OFFSET :offset;\
        ")
    
    return_val = db.execute(stmt, {"id_marca": marca.id_marca, "limit": limit, "offset": offset}).mappings().all()
    
    return marcas.MarcaProdutosResponse(
        **marca.__dict__, 
        produtos=return_val, 
        paginacao={
            "offset": offset, 
            "limit": limit, 
            "total": db.query(ProdutosDB)\
                .join(MarcasDB)\
                .filter(MarcasDB.id_marca == marca.id_marca)\
                .count()
            }
        )