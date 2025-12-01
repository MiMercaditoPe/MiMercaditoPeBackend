from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://adminmercadito:Mercadito2025"
    "@mimercaditope-server.database.windows.net:1433/MiMercadito-db"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
    "&Connection+Timeout=30"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=True  # pon true para ver errores claros
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
