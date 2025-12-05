from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


from routers.compras import router as compras_router

app = FastAPI(title="Mi Mercadito Pe - Backend Oficial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Cargando datos iniciales...")

df_precios = pd.read_csv("data/dataset_compras_completo.csv", encoding="utf-8")
df_tiendas = pd.read_csv("data/tiendas.csv", encoding="utf-8")

print("Datos cargados correctamente")

app.state.df_precios = df_precios
app.state.df_tiendas = df_tiendas

app.include_router(compras_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Backend Mi Mercadito Pe funcionando al 100%"}
