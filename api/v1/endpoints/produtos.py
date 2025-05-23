# Imports de todos os endpoints
from fastapi import APIRouter, Query, Path
from typing import Annotated, List, Union
from sqlalchemy import update, text, select, and_, func
from sqlalchemy.orm import Bundle
from main import db_dependency

from models.db_models import ProdutosDB, ProdutoListadoDB, MarcasDB, CategoriasDB
from models.schemas import produtos, em_kit, em_variacao, produto_listado

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get('/', name='Buscar produtos', description="Busca todos os produtos")
async def get_produtos(
    produto_query: produtos.ProdutoQuery = produtos.ProdutoQuery.as_query(),
    limit: int = 10,
    offset: int = 0,
    db: db_dependency = None
) -> produtos.ProdutoFullListingResponse:
    filters = produto_query.model_dump(exclude_defaults=True, exclude_none=True)

    conditions = []
    for field, value in filters.items():
        if hasattr(ProdutosDB, field):
            conditions.append(getattr(ProdutosDB, field) == value)
    
    stmt = (
        select(
            ProdutosDB,
            MarcasDB.descritivo_marca.label("marca_nome"),
            CategoriasDB.descritivo_categoria.label("categoria_nome")
        )
        .join(MarcasDB, MarcasDB.id_marca == ProdutosDB.marca_prod, isouter=True)
        .join(CategoriasDB, CategoriasDB.id_categoria == ProdutosDB.categoria_prod, isouter=True)
        .where(and_(*conditions))
        .order_by(ProdutosDB.id_prod.asc())
        .offset(offset)
        .limit(limit)
    )
    
    rows = db.execute(stmt).all()
    
    produtos_list = []
    for produto, marca_nome, categoria_nome in rows:
        produto_dict = {
            **produto.__dict__,
            "marca_prod": marca_nome,
            "categoria_prod": categoria_nome
        }
        produto_dict.pop("_sa_instance_state", None)
        produtos_list.append(produto_dict)
    
    return {
        'produtos': produtos_list, 
        'paginacao': {
            'limit': limit, 
            'offset': offset, 
            'total': 
                db.execute(select(func.count())\
                .select_from(ProdutosDB)\
                .join(MarcasDB, MarcasDB.id_marca == ProdutosDB.marca_prod, isouter=True)\
                .join(CategoriasDB, CategoriasDB.id_categoria == ProdutosDB.categoria_prod, isouter=True)\
                .where(and_(*conditions)))\
                .scalar()}}

@router.post('/', name='Inserir produtos', description='Insere um ou mais produtos ao banco de dados')
async def inser_produtos(
    produtos: Union[produtos.ProdutoCreate, List[produtos.ProdutoCreate]],
    db: db_dependency = None
):
    if isinstance(produtos, list):
        for produto in produtos:
            produto_db = ProdutosDB(**produto.model_dump())
            db.add(produto_db)
    else:
        produto_db = ProdutosDB(**produtos.model_dump())
        db.add(produto_db)
    db.commit()
    return {"msg": "produto(s) inserido(s) com sucesso!"}

@router.patch('/', name='Alterar produto', description='Altera os dados de um produto específico')
async def update_produto(
    id_prod: Annotated[int, Query(description="Id do produto que será alterado")],
    produto: produtos.ProdutoPatch,
    db: db_dependency
):
    stmt = update(ProdutosDB).where(ProdutosDB.id_prod == id_prod).values(**produto.model_dump(exclude_defaults=True, exclude_none=True))
    db.execute(stmt)
    db.commit()
    
@router.delete('/', name='Desativar produto', description='Desativa um produto')
async def delete_produto(
    id_prod: Annotated[int, Query(description="Id do produto que será desativado")],
    db: db_dependency
):
    if not db.get(ProdutosDB, id_prod).ativo_prod:
        return {"msg": "Produto já está desativado"}
    else:
        stmt = update(ProdutosDB).where(ProdutosDB.id_prod == id_prod).values(ativo_prod = False)
        db.execute(stmt)
        db.commit()
        return {"msg": "Produto desativado com sucesso!"}
    
@router.patch('/ativar', name='Reativar produto', description='Reativa um produto')
async def reativar_produto(
    id_prod: Annotated[int, Query(description="Id do produto que será reativado")],
    db: db_dependency
): 
    if db.get(ProdutosDB, id_prod).ativo_prod:
        return {"msg": "Produto já está ativo"}
    else:
        stmt = update(ProdutosDB).where(ProdutosDB.id_prod == id_prod).values(ativo_prod = True)
        db.execute(stmt)
        db.commit()
        return {"msg": "Produto reativado com sucesso!"}
    
@router.get('/{id_prod}/composicao', name='Buscar composição', description='Busca todos os produtos que fazem parte de um kit')
async def get_composicao(
    id_prod: Annotated[str, Path(description="Id do produto kit")],
    db: db_dependency
) ->  em_kit.ProdutoKitResponse:
    
    produto = db.get(ProdutosDB, id_prod)
    stmt = text("\
        select p2.*, k.quant_por_kit\
        from kits k\
        join produtos p1 on k.id_prod_pai = p1.id_prod\
        join produtos p2 on k.id_prod_filho = p2.id_prod\
        where p1.id_prod = :id_prod_value;"
    )
    db_resp = db.execute(stmt, {"id_prod_value": id_prod}).mappings().all()
    
    return_val = em_kit.ProdutoKitResponse(**produto.__dict__, kit_contem=db_resp)
    
    return return_val

@router.get('/{id_prod}/kits', name='Buscar kits que faz parte', description='Retorna todos os kits que tem o produto buscado na sua composição')
async def get_kits(
    id_prod: Annotated[str, Path(description="Id do produto composição")],
    limit: Annotated[int, Query(description="Quantidade máxima de respostas", gt=1, le=100)] = 10,
    offset: Annotated[int, Query(description="Quantidade de valores que devem ser 'pulados'")] = 0,
    db: db_dependency = None
) ->  em_kit.ProdutoComposicaoResponse:
    
    produto = db.get(ProdutosDB, id_prod)
    stmt = text("\
        select p2.*, k.quant_por_kit\
        from kits k\
        join produtos p1 on k.id_prod_filho = p1.id_prod\
        join produtos p2 on k.id_prod_pai = p2.id_prod\
        where p1.id_prod = :id_prod_value\
        offset :offset\
        limit :limit\
        ;"
    )
    db_resp = db.execute(stmt, {"id_prod_value": id_prod, "offset": offset, "limit": limit}).mappings().all()
    
    return_val = em_kit.ProdutoComposicaoResponse(
        **produto.__dict__, 
        faz_parte_de={
            "produtos": db_resp, 
            "paginacao": {
                "limit": limit,
                "offset": offset,
                "total": len(db_resp) # FIXME É necessário encontrar uma maneira melhor de pegar a quantidade total de itens
            }})
    
    return return_val

@router.get('/{id_prod}/variacoes', name='Buscar variações', description='Retorna todas as variações de um produto')
async def get_variacoes(
    id_prod: Annotated[str, Path(description="Id do produto")],
    db: db_dependency
) -> em_variacao.ProdutoPaiVarResponse: 
    produto = db.get(ProdutosDB, id_prod)
    
    stmt = text("\
        select p2.*\
        from produtos p1\
        join variacoes v on v.id_prod_pai = p1.id_prod\
        join produtos p2 on p2.id_prod = v.id_prod_filho\
        where p1.id_prod = :id_prod_value;"
    )
    db_resp = db.execute(stmt, {"id_prod_value": id_prod}).mappings().all()
    
    return_val = em_variacao.ProdutoPaiVarResponse(**produto.__dict__, variacoes=db_resp)
    
    return return_val

@router.get('/{id_prod}/variacao_de', name='Buscar se é variação', description='Retorna o pai da variação buscada, caso não retorne nada, o produto inserido não é uma variação')
async def get_pai_variacao(
    id_prod: Annotated[str, Path(description="Id do produto")],
    db: db_dependency
) -> em_variacao.ProdutoFilhoVarResponse: 
    produto = db.get(ProdutosDB, id_prod)
    
    stmt = text("\
        select p2.*\
        from produtos p1\
        join variacoes v on v.id_prod_filho = p1.id_prod\
        join produtos p2 on p2.id_prod = v.id_prod_pai\
        where p1.id_prod = :id_prod_value;"
    )
    db_resp = db.execute(stmt, {"id_prod_value": id_prod}).mappings().all()
    
    return_val = em_variacao.ProdutoFilhoVarResponse(**produto.__dict__, e_variacao_de=db_resp)
    
    return return_val

@router.post('/listar', name='Inserir listagens', description='Insere uma ou mais listagens de produtos')
async def insert_listagens(
    produtos_listados: Union[produto_listado.ProdutoListadoCreate, List[produto_listado.ProdutoListadoCreate]],
    db: db_dependency
):
    if isinstance(produtos_listados, list):
        for listagem in produtos_listados:
            prod_listado_db = ProdutoListadoDB(**listagem.model_dump())
            db.add(prod_listado_db)
    else:
        prod_listado_db = ProdutoListadoDB(**produtos_listados.model_dump())
        db.add(prod_listado_db)
    db.commit()
            
@router.get('/listagens', name='Buscar listagens', description='Retorna todas as listagens do produto com a empresa que listou e o marketplace onde foi listado')
async def get_listagens(
    id_prod: Annotated[int, Query(description="Id do produto")],
    db: db_dependency
) -> produtos.ProdutoListagens:
    stmt = text('\
        SELECT e.descritivo_empresa as empresa, m.descritivo_marketplace as marketplace, pl.codigo_marketplace as codigo_marketplace, pl.preco_marketplace as preco_marketplace\
        FROM produtos p \
        JOIN "produtoListado" pl ON pl.id_produto = p.id_prod\
        JOIN "vendeEm" ve ON ve.id_vende_em = pl.id_vende_em\
        JOIN empresas e ON e.id_empresa = ve.id_empresa\
        JOIN marketplaces m ON m.id_marketplace = ve.id_marketplace\
        WHERE p.id_prod = :id_prod;')
    
    return {
        **db.get(ProdutosDB, id_prod).__dict__, 
        "listagens": db.execute(stmt, {'id_prod': id_prod}).mappings().all()}  