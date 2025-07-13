# leyendas-cr-backend/app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings # Importamos las configuraciones, incluyendo SECRET_KEY y ALGORITHM

# Configuración para el hashing de contraseñas
# Usamos bcrypt, que es un algoritmo de hashing seguro y recomendado.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funciones para Hashing de Contraseñas ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con una contraseña hasheada.

    Args:
        plain_password (str): La contraseña sin hashear.
        hashed_password (str): La contraseña previamente hasheada almacenada en la DB.

    Returns:
        bool: True si las contraseñas coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de una contraseña en texto plano.

    Args:
        password (str): La contraseña en texto plano.

    Returns:
        str: La contraseña hasheada.
    """
    return pwd_context.hash(password)

# --- Funciones para JWT (JSON Web Tokens) ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JSON Web Token (JWT) de acceso.

    Args:
        data (dict): Un diccionario con los datos a incluir en el token (ej. {"sub": "user@example.com"}).
        expires_delta (Optional[timedelta]): La duración opcional para la expiración del token.
                                             Si no se provee, usa el valor por defecto de las configuraciones.

    Returns:
        str: El token JWT codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Usa la configuración de tiempo de expiración por defecto
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire}) # Añade el timestamp de expiración al payload
    # Codifica el token usando el SECRET_KEY y el algoritmo definidos en las configuraciones
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verifica y decodifica un JSON Web Token (JWT).

    Args:
        token (str): El token JWT a verificar.

    Returns:
        Optional[dict]: El payload decodificado del token si es válido, None en caso contrario.
    """
    try:
        # Decodifica el token usando el SECRET_KEY y el algoritmo
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # Captura cualquier error relacionado con el JWT (token inválido, expirado, etc.)
        return None