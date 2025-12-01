from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.compras import router as compras_router
from database import Base, engine, SessionLocal

# Crear tablas si aún no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Mercadito Pe - Backend Oficial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Backend Mi Mercadito Pe funcionando con Azure SQL"}

# IMPORTANTE: pasar la dependencia al router
app.include_router(
    compras_router,
    prefix="/api",
    dependencies=[]  # o agregar aquí get_db si el router lo usa
)
