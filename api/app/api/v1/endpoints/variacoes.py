# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union
from sqlalchemy import update, text, delete
from app.main import db_dependency

from models.db_models import VariacoesDB
from models.schemas import variacoes

router = APIRouter(prefix="/variacoes", tags=["Variações"])

@router.get('/')
async def get_variacoes(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> variacoes.VariacaoListingResponse:
    stmt = db.query(VariacoesDB)
    variacoes_data = stmt.order_by(VariacoesDB.id_variacao.asc()).limit(limit).offset(offset)
    return {
        'variacoes': variacoes_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}} 

@router.post('/')
async def insert_variacao(
    variacoes: Union[variacoes.VariacaoCreate, List[variacoes.VariacaoBase]],
    db: db_dependency = None
):
    if isinstance(variacoes, list):
        for variacao in variacoes:
            variacao_db = VariacoesDB(**variacao.model_dump())
            db.add(variacao_db)
    else:
        variacao_db = VariacoesDB(**variacoes.model_dump())
        db.add(variacao_db)
    db.commit()
    return {"msg": "Variação(ões) inserida(s) com sucesso!"}

@router.delete('/')
async def delete_variacao(
    id_variacao: Annotated[int, Query(description="Id da variação que será deletada")],
    db: db_dependency
): 
    stmt = delete(VariacoesDB).where(VariacoesDB.id_variacao == id_variacao)
    db.execute(stmt)
    db.commit()