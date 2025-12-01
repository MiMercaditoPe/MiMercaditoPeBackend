from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambia tu cadena de conexión real aquí
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://adminmercadito:Mercadito2025@mimercaditope-server.database.windows.net:1433/MiMercadito-db?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"

# Crear engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()