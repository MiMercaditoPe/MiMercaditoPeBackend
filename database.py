import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=mimercaditope-server.database.windows.net,1433;"
    "DATABASE=MiMercadito-db;"
    "UID=adminmercadito;"
    "PWD=Mercadito2025;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

cursor = conn.cursor()
cursor.execute("SELECT TOP 1 name FROM sys.tables")
row = cursor.fetchone()

print("Conexión exitosa. Tabla encontrada:", row)
