# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union, Optional
from sqlalchemy import update, text, delete
from main import db_dependency

from models.db_models import AgendamentosDB, EmAgendamentoDB
from models.schemas import agendamentos, em_agendamento

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.get('/')
async def get_agendamentos(
    limit: Annotated[int, Query(description="Limite de valores que podem ser respondidos", ge=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidades de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
)-> agendamentos.AgendamentoListingResponse:
    stmt = db.query(AgendamentosDB)
    agendamento_data = stmt.order_by(AgendamentosDB.id_agendamento.asc()).limit(limit).offset(offset)
    return {
        'agendamentos': agendamento_data, 
        'paginacao': {'limit': limit, 'offset': offset, 'total': stmt.count()}} 

@router.post('/')
async def insert_agendamentos(
    agendamentos: Union[agendamentos.AgendamentoCreate, List[agendamentos.AgendamentoCreate]],
    db: db_dependency = None
):
    if isinstance(agendamentos, list):
        for agendamento in agendamentos:
            agendamento_db = AgendamentosDB(**agendamento.model_dump())
            db.add(agendamento_db)
    else:
        agendamento_db = AgendamentosDB(**agendamentos.model_dump())
        db.add(agendamento_db)
    db.commit()
    return {"msg": "Agendamentos(s) inserido(s) com sucesso!"}

@router.patch('/')
async def update_agendamento(
    id_agendamento: Annotated[int, Query(description="Id da agendamento que será alterada")],
    agendamento: agendamentos.AgendamentoPatch,
    db: db_dependency
): 
    stmt = update(AgendamentosDB).where(AgendamentosDB.id_agendamento == id_agendamento).values(**agendamento.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()
    
@router.delete('/')
async def delete_agendamento(
    id_agendamento: Annotated[int, Query(description="Id do agendamento que será deletado")],
    db: db_dependency
): 
    stmt = delete(AgendamentosDB).where(AgendamentosDB.id_agendamento == id_agendamento)
    db.execute(stmt)
    db.commit()
    
@router.get('/{id_agendamento}/produtos')
async def get_agendamento_produtos(
    id_agendamento: Annotated[int, Path(description="Id do agendamento que será buscado")],
    db: db_dependency
) -> em_agendamento.AgendamentoProdutoResponse:
    agendamento = db.get(AgendamentosDB, id_agendamento)
    
    stmt = text(' \
        SELECT p.*, ea.quant_produto as quant_prod \
        FROM agendamentos a \
        JOIN "emAgendamento" ea ON ea.id_agendamento = a.id_agendamento \
        JOIN "produtoListado" pl ON pl.id_produto_listado = ea.id_produto_listado \
        JOIN produtos p ON p.id_prod = pl.id_produto \
        WHERE a.id_agendamento = :id_agendamento;'
        )
    
    return {**agendamento.__dict__, "produtos": db.execute(stmt, {'id_agendamento': id_agendamento}).mappings().all()}

@router.post('/agendar')
async def insert_agendamento_produto(
    em_agendamento: Union[em_agendamento.EmAgendamentoCreate, List[em_agendamento.EmAgendamentoCreate]],
    db: db_dependency
):
    if isinstance(em_agendamento, list):
        for agendamento in em_agendamento:
            em_agendamento_db = EmAgendamentoDB(**agendamento.model_dump())
            db.add(em_agendamento_db)
    else:
        em_agendamento_db = EmAgendamentoDB(**em_agendamento.model_dump())
        db.add(em_agendamento_db)
    db.commit()