# app/db/database.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Crear el motor de la base de datos síncrono
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.DEBUG if hasattr(settings, 'DEBUG') else False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_timeout=30,
    # Configuraciones adicionales para MySQL
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
        "autocommit": False,
    }
)

# Fábrica de sesiones síncronas
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Base declarativa para tus modelos
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    logger.debug("🔌 Conexión a DB establecida")
    try:
        yield db
    except Exception:
        # Captura tanto errores de SQLAlchemy como cualquier otro
        logger.exception("💥 Error en BD; deshaciendo transacción")
        db.rollback()
        raise
    finally:
        logger.debug("🔒 Conexión a DB cerrada")
        db.close()