"""Configuração do banco de dados (MySQL via env ou SQLite local)."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Se não houver DATABASE_URL, cai no SQLite em ./data/easyorder.db
DEFAULT_SQLITE_URL = "sqlite:///./data/easyorder.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependência para obter a sessão de banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
