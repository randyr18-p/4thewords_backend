# leyendas-cr-backend/app/db/models.py

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 

from app.db.database import Base 

# --- Modelo Usuario ---
class Usuario(Base):
    __tablename__ = "usuarios" 

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(255), unique=True, nullable=False, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    role = Column(Enum('admin', 'reader'), default='reader', nullable=False) 
    is_active = Column(Boolean, default=True, nullable=False) 
    is_verified = Column(Boolean, default=False, nullable=False) 
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    ultima_modificacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)



# --- Modelo Categoria ---
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)

    # Relación inversa: una categoría puede tener muchas leyendas
    leyendas = relationship("Leyenda", back_populates="categoria")


# --- Modelo Provincia ---
class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False, index=True)

    # Relaciones inversas: una provincia tiene muchos cantones y muchas leyendas
    cantones = relationship("Canton", back_populates="provincia")
    leyendas = relationship("Leyenda", back_populates="provincia")


# --- Modelo Canton ---
class Canton(Base):
    __tablename__ = "cantones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)

    # Relación: un cantón pertenece a una provincia
    provincia = relationship("Provincia", back_populates="cantones")
    # Relación inversa: un cantón tiene muchos distritos y muchas leyendas
    distritos = relationship("Distrito", back_populates="canton")
    leyendas = relationship("Leyenda", back_populates="canton")


# --- Modelo Distrito ---
class Distrito(Base):
    __tablename__ = "distritos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    canton_id = Column(Integer, ForeignKey("cantones.id"), nullable=False)

    # Relación: un distrito pertenece a un cantón
    canton = relationship("Canton", back_populates="distritos")
    # Relación inversa: un distrito tiene muchas leyendas
    leyendas = relationship("Leyenda", back_populates="distrito")


# --- Modelo Leyenda ---
class Leyenda(Base):
    __tablename__ = "leyendas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False, index=True)
    texto_descriptivo = Column(Text, nullable=False)
    imagen_url = Column(String(500), nullable=False)
    fecha_leyenda = Column(Date, nullable=False) # Fecha en que se originó/relata la leyenda
    fecha_publicacion = Column(DateTime, default=func.now(), nullable=False) # Fecha de publicación en la app
    fuente = Column(String(255), nullable=True) # Puede ser opcional
    autor_leyenda = Column(String(255), nullable=True) # Puede ser opcional
    ultima_actualizacion = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Claves Foráneas
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    canton_id = Column(Integer, ForeignKey("cantones.id"), nullable=False)
    distrito_id = Column(Integer, ForeignKey("distritos.id"), nullable=False)

    # Relaciones con otras tablas
    categoria = relationship("Categoria", back_populates="leyendas")
    provincia = relationship("Provincia", back_populates="leyendas")
    canton = relationship("Canton", back_populates="leyendas")
    distrito = relationship("Distrito", back_populates="leyendas")
