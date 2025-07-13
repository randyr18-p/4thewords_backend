from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de base de datos 
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost:3306/dbname"

    # Configuración de desarrollo/producción
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Configuración de pool de conexiones 
    DB_POOL_SIZE: int = 15        # Aumentado para compensar bloqueo
    DB_MAX_OVERFLOW: int = 25     # Más conexiones overflow
    DB_POOL_RECYCLE: int = 3600   # Reciclar conexiones cada hora
    DB_POOL_TIMEOUT: int = 30     # Timeout para obtener conexión

    # Configuración de seguridad y JWT
    SECRET_KEY: str
    ALGORITHM: str                # e.g. "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int  # en minutos

    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None

    # Configuración específica para MySQL
    MYSQL_CHARSET: str = "utf8mb4"
    MYSQL_AUTOCOMMIT: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()
