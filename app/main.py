"""Módulo principal da aplicação FastAPI EasyOrder."""

# External libraries
from fastapi import FastAPI

# Internal libraries
from app.routers.pedidos import router as pedidos_router
from app.routers.clientes import router as clientes_router
from app.routers.relatorios import router as relatorios_router
from app.routers.produtos import router as produtos_router
from app.routers.produtos import router as pagamentos_router
from app.database import Base, engine


# Cria todas as tabelas no banco
Base.metadata.create_all(bind=engine)

# Inicializa a aplicação
app = FastAPI(
    title="EasyOrder API",
    description="API para gerenciamento de pedidos e clientes.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """
    Rota raiz da API.

    Returns:
        dict: Mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo ao EasyOrder!"}


# Inclui os routers existentes
app.include_router(pedidos_router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(relatorios_router, prefix="/relatorios", tags=["Relatórios"])
app.include_router(produtos_router)
app.include_router(pagamentos_router) 
