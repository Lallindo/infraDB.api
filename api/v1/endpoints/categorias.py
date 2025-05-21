# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union, Optional
from sqlalchemy import update, text, delete
from main import db_dependency

from models.db_models import CategoriasDB, ProdutosDB
from models.schemas import categorias

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get('/')
async def get_categorias(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> categorias.CategoriaListingResponse:
    stmt = db.query(CategoriasDB)
    categorias_data = stmt.order_by(CategoriasDB.id_categoria.asc()).limit(limit).offset(offset)
    return {
        'categorias': categorias_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}}
    
@router.post('/')
async def insert_categorias(
    categorias: Union[categorias.CategoriaCreate, List[categorias.CategoriaCreate]],
    db: db_dependency = None
):
    if isinstance(categorias, list):
        for categoria in categorias:
            categoria_db = CategoriasDB(**categoria.model_dump())
            db.add(categoria_db)
    else:
        categoria_db = CategoriasDB(**categorias.model_dump())
        db.add(categoria_db)
    db.commit()
    return {"msg": "Categoria(s) inserida(s) com sucesso!"}

@router.patch('/')
async def update_categoria(
    id_categoria: Annotated[int, Query(description="Id da categoria que será alterada")],
    categoria: categorias.CategoriaPatch,
    db: db_dependency
):
    stmt = update(CategoriasDB).where(CategoriasDB.id_categoria == id_categoria).values(**categoria.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()
    
@router.delete('/')
async def delete_categoria(
    id_categoria: Annotated[int, Path(description="Id da categoria que será deletada")],
    db: db_dependency
):
    stmt = delete(CategoriasDB).where(CategoriasDB.id_categoria == id_categoria)
    db.execute(stmt)
    db.commit()

@router.get('/produtos', description="Busca todos os produtos relacionados com uma categoria. Caso Id e Nome sejam fornecidos, Id será priorizado.")
async def get_produtos_categorias(
    id_categoria: Annotated[Optional[int], Query(description="Id da categoria")] = None,
    nome_categoria: Annotated[Optional[str], Query(description="Nome da categoria")] = None,
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
):
    if id_categoria is not None:
        categoria = db.get(CategoriasDB, id_categoria)
    elif nome_categoria is not None:
        categoria = db.query(CategoriasDB).where(CategoriasDB.descritivo_categoria.contains(nome_categoria)).first()
    else:
        return {"msg": "Envie Id ou Nome para buscar"}
        
    stmt = text("\
        SELECT p.*\
        FROM categorias c\
        JOIN produtos p ON p.categoria_prod = c.id_categoria\
        WHERE c.id_categoria = :id_categoria\
        LIMIT :limit\
        OFFSET :offset;\
        ")
    
    return_val = db.execute(stmt, {"id_categoria": categoria.id_categoria, "limit": limit, "offset": offset}).mappings().all()
    
    return categorias.CategoriaProdutosResponse(
        **categoria.__dict__, 
        produtos=return_val, 
        paginacao={
            "offset": offset, 
            "limit": limit, 
            "total": db.query(ProdutosDB)\
                .join(CategoriasDB)\
                .filter(CategoriasDB.id_categoria == categoria.id_categoria)\
                .count()
            }
        )