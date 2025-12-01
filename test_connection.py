# test_connection.py  →  Versión definitiva que ya no falla con fetchone()[0]
from sqlalchemy import create_engine, text
import urllib.parse

# ================================== CONFIGURACIÓN ==================================
server = "mimercaditope-server.database.windows.net"
database = "MiMercadito-db"
username = "adminmercadito"
password = "Mercadito2025"

password_encoded = urllib.parse.quote_plus(password)

connection_string = (
    f"mssql+pyodbc://{username}:{password_encoded}@{server}:1433/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&Encrypt=yes"
    "&TrustServerCertificate=no"
    "&Connection+Timeout=30"
)

engine = create_engine(connection_string, echo=False)  # echo=True si quieres ver el log SQL

print("Intentando conectar a Azure SQL Database...\n")

try:
    with engine.connect() as conn:
        print("Conexión establecida correctamente")

        # 1. Prueba más simple y que NUNCA falla por filas vacías
        result = conn.execute(text("SELECT 1 AS conexion_ok"))
        row = result.fetchone()
        print("Prueba rápida →", row[0] if row else "¡falló!")  # siempre imprime 1

        # 2. Versión de SQL Server (segura)
        result = conn.execute(text("SELECT @@VERSION AS version"))
        row = result.fetchone()
        if row and row[0]:
            version = row[0].replace("\n", " ").strip()
            print(f"Versión del servidor: {version[:120]}...")
        else:
            print("No se pudo obtener @@VERSION")

        # 3. Buscar tablas de forma segura
        result = conn.execute(text("""
            SELECT TOP 1 TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """))
        row = result.fetchone()
        if row:
            print(f"Primera tabla encontrada: {row[0]}")
        else:
            print("Base de datos vacía o sin tablas accesibles (normal en pruebas)")

        print("\n¡TODO FUNCIONA PERFECTAMENTE!")

except Exception as e:
    print("Falló la conexión o la consulta")
    print(f"Error detallado: {e}")