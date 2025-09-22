"""Módulo principal da aplicação FastAPI EasyOrder."""

import logging
import os
from fastapi import FastAPI
from watchtower import CloudWatchLogHandler

# Internal libraries
from app.routers.pedidos import router as pedidos_router
from app.routers.clientes import router as clientes_router
from app.routers.relatorios import router as relatorios_router
from app.routers.produtos import router as produtos_router
from app.routers.pagamentos import router as pagamentos_router
from app.routers.entregas import router as entregas_router

LOG_GROUP_NAME = os.getenv("LOG_GROUP_NAME", "/easyorder/api")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "sa-east-1")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if os.getenv("TEST_ENV") != "true":
    try:
        cw_handler = CloudWatchLogHandler(
            log_group_name=LOG_GROUP_NAME,
            region_name=AWS_REGION,
        )
        logger.addHandler(cw_handler)
        logger.info("✅ CloudWatch LogHandler inicializado com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Falha ao inicializar CloudWatchLogHandler: {e}")

app = FastAPI(
    title="EasyOrder API",
    description="API para gerenciamento de pedidos e clientes.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Loga um evento quando a API inicia."""
    logger.info("🚀 API Iniciada e pronta para receber requisições.")


@app.get("/")
def read_root():
    """Rota raiz da API."""
    logger.info("🏠 Rota raiz acessada com sucesso por um cliente.")
    return {"message": "Bem-vindo ao EasyOrder! Monitoramento Ativo!"}


# Routers
app.include_router(pedidos_router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(relatorios_router, prefix="/relatorios", tags=["Relatórios"])
app.include_router(produtos_router, prefix="/produtos", tags=["Produtos"])
app.include_router(pagamentos_router, prefix="/pagamentos", tags=["Pagamentos"])
app.include_router(entregas_router, prefix="/entregas", tags=["Entregas"])
