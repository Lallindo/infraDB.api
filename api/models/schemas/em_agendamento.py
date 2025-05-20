from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .response import ResponseBase
from .agendamentos import AgendamentoResponse
from .produtos import ProdutoResponse

class EmAgendamentoBase(BaseModel):
    id_agendamento: int = Field(description="Id do agendamento")
    id_produto_listado: int = Field(description="Id do produto")
    quant_produto: int = Field(description="Quantidade do produto no agendamento")

class EmAgendamentoCreate(EmAgendamentoBase):
    pass

class EmAgendamentoResponse(EmAgendamentoBase):
    id_em_agendamento: int = Field(description="Id da relação entre um produto e o agendamento")

class EmAgendamentoPatch(EmAgendamentoCreate):
    pass

class EmAgendamentoListingResponse(BaseModel):
    em_agendamentos: List[EmAgendamentoResponse]
    paginacao: ResponseBase
    
class ProdutoQuantidadeAgendResponse(ProdutoResponse):
    quant_prod: int = Field(description="Quantidade do produto no agendamento")
    
class AgendamentoProdutoResponse(AgendamentoResponse):
    produtos: List[ProdutoQuantidadeAgendResponse]