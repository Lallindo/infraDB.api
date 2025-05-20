from fastapi import APIRouter
from .endpoints.produtos import router as produto_router
from .endpoints.kits import router as kit_router
from .endpoints.variacoes import router as variacao_router
from .endpoints.marcas import router as marca_router
from .endpoints.categorias import router as categoria_router
from .endpoints.empresas import router as empresa_router
from .endpoints.marketplaces import router as marketplace_router
from .endpoints.agendamentos import router as agendamento_router

router = APIRouter()

router.include_router(produto_router)
router.include_router(kit_router)
router.include_router(variacao_router)
router.include_router(marca_router)
router.include_router(categoria_router)
router.include_router(empresa_router)
router.include_router(marketplace_router)
router.include_router(agendamento_router)