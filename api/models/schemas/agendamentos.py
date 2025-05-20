from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .response import ResponseBase

class AgendamentoBase(BaseModel):
    codigo_agendamento: str = Field(default="codigo", description="Código do agendamento dentro do marketplace que ele faz parte")
    data_agendamento: datetime = Field(default=datetime.now(), description="Data da criação do agendamento") 

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id_agendamento: int = Field(description="Id do agendamento")

class AgendamentoPatch(AgendamentoCreate):
    pass

class AgendamentoListingResponse(BaseModel):
    agendamentos: List[AgendamentoResponse]
    paginacao: ResponseBase