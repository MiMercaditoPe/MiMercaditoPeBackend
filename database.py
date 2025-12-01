# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from sqlalchemy import text

# Usa tu cadena real
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://adminmercadito:Mercadito2025@mimercaditope-server.database.windows.net:1433/MiMercadito-db?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"

# Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Sesión
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base para modelos (si usas ORM)
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
