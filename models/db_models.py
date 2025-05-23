from sqlalchemy import String, ForeignKey, DECIMAL, Enum, Date, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from typing import get_args, Literal, List
import datetime
import enum
from config import get_conn_string

class Base(DeclarativeBase):
    pass

TiposProd = Literal["kit", "simples", "outro"]

class ProdutosDB(Base):
    __tablename__ = "produtos"
    
    id_prod: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    marca_prod: Mapped[int] = mapped_column(ForeignKey("marcas.id_marca"), nullable=True)
    categoria_prod: Mapped[int] = mapped_column(ForeignKey("categorias.id_categoria"), nullable=True)
    id_tiny_prod: Mapped[str] = mapped_column(String(100)) 
    sku_prod: Mapped[str] = mapped_column(String(50), index=True)
    descritivo_prod: Mapped[str] = mapped_column(String(200), index=True)
    gtin_prod: Mapped[str] = mapped_column(String(100), index=True)
    estoque_prod: Mapped[int] = mapped_column(nullable=True)
    preco_prod: Mapped[float] = mapped_column(DECIMAL(10, 2))
    custo_prod: Mapped[float] = mapped_column(DECIMAL(10, 2))
    localizacao_prod: Mapped[str] = mapped_column(String(300), nullable=True)
    tipo_prod: Mapped[str] = mapped_column(Enum(
        *get_args(TiposProd), 
        name='tipo_prod', 
        create_constraint=True, 
        validate_strings=True
    ))
    ativo_prod: Mapped[bool] = mapped_column(default=True) 
    
class KitsDB(Base):
    __tablename__ = "kits"
    
    id_kit: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_prod_pai: Mapped[int] = mapped_column(ForeignKey("produtos.id_prod"))
    id_prod_filho: Mapped[int] = mapped_column(ForeignKey("produtos.id_prod"))
    quant_por_kit: Mapped[int] = mapped_column()
    
    
class VariacoesDB(Base):
    __tablename__ = "variacoes"
    
    id_variacao: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_prod_pai: Mapped[int] = mapped_column(ForeignKey("produtos.id_prod")) # Pai das variações
    id_prod_filho: Mapped[int] = mapped_column(ForeignKey("produtos.id_prod")) # Variação
    # ! Teoricamente, a melhor estrutura seria ter as variações apenas dentro dessa tabela, ou seja:
    # ? 1 - Produto é registrado e possúi variações, produto pai recebe um sku, por exemplo: JP1234;
    # ? 2 - Suas variações são registradas nessa table e recebem uma "adição", um valor que será adicionado ao SKU de seu pai, por exemplo: 1, 2, 3, 4;
    # ? 3 - Variações são devolvidas com o SKU unido, ou seja: JP1234-1, JP1234-2, JP1234-3...;
    
    """
    ! Essa seria a estrutura "mais correta", como o sistema já está "bagunçado" a ideia será:
    ? 1 - Pessoa, na aplicação, decide criar uma variação;
    ? 2 - Dados da variação são inseridos como um novo produto;
    ? 3 - Id do novo produto é relacionado com o Id pai e a variação é criada; 
    codigo_variacao: Mapped[int] = mapped_column()
    cor_variacao: Mapped[str] = mapped_column() # Trocar para ENUM
    tamanho_variacao: Mapped[str] = mapped_column() # Trocar para ENUM
    """
     
     
class MarcasDB(Base):
    __tablename__ = "marcas"
    
    id_marca: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    descritivo_marca: Mapped[str] = mapped_column(String(100))
    
    
class CategoriasDB(Base):
    __tablename__ = "categorias"
    
    id_categoria: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    descritivo_categoria: Mapped[str] = mapped_column(String(100))

class ProdutoListadoDB(Base):
    __tablename__ = "produtoListado"
    
    id_produto_listado: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_produto: Mapped[int] = mapped_column(ForeignKey("produtos.id_prod"))
    id_vende_em: Mapped[int] = mapped_column(ForeignKey("vendeEm.id_vende_em"))
    codigo_marketplace: Mapped[str] = mapped_column(String(1000), nullable=True, default=None)
    preco_marketplace: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True, default=None)
    
    
class VendeEmDB(Base):
    __tablename__ = "vendeEm"
    
    id_vende_em: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_empresa: Mapped[int] = mapped_column(ForeignKey("empresas.id_empresa"))
    id_marketplace: Mapped[int] = mapped_column(ForeignKey("marketplaces.id_marketplace"))
    

class EmpresasDB(Base):
    __tablename__ = "empresas"
    
    id_empresa: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    descritivo_empresa: Mapped[str] = mapped_column(String(50))
    
    
class MarketplacesDB(Base):
    __tablename__ = "marketplaces"
    
    id_marketplace: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    descritivo_marketplace: Mapped[str] = mapped_column(String(50))
    
    
class AgendamentosDB(Base):
    __tablename__ = "agendamentos"
    
    id_agendamento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    data_agendamento: Mapped[datetime.datetime] = mapped_column()
    codigo_agendamento: Mapped[str] = mapped_column(String(100))
    
    
class EmAgendamentoDB(Base):
    __tablename__ = "emAgendamento"
    
    id_em_agendamento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    id_agendamento: Mapped[int] = mapped_column(ForeignKey("agendamentos.id_agendamento"))
    id_produto_listado: Mapped[int] = mapped_column(ForeignKey("produtoListado.id_produto_listado"))
    quant_produto: Mapped[int] = mapped_column()
    

connection_string = get_conn_string('postgresql')   
engine = create_engine(connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)