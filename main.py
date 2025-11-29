# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

from algoritmos.algoritmo_backtracking import calcular_mejores_tiendas
from algoritmos.algoritmo_rutas_mst import kruskal_tienda_mas_cercana

app = FastAPI(title="Mi Mercadito Pe - Backend Oficial")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga única de datos
print("Cargando datos...")
df_precios = pd.read_csv("data/dataset_compras_completo.csv", encoding="utf-8")
df_tiendas = pd.read_csv("data/tiendas.csv", encoding="utf-8")
print(f"Listo: {len(df_precios)} precios, {len(df_tiendas)} tiendas")

# Modelos
class ProductoInput(BaseModel):
    nombre: str
    cantidad: Optional[float] = 1.0
    prioridad: str = "media"

class CompraRequest(BaseModel):
    distrito_usuario: str
    presupuesto: float
    productos: List[ProductoInput]

class TiendaResultado(BaseModel):
    nombre_tienda: str
    distrito: str
    precio_total: float
    ahorro: float = 0.0

class CompraResponse(BaseModel):
    mejores_tiendas: List[TiendaResultado]
    tienda_mas_cercana: str
    precio_mas_bajo: float
    mensaje: str = "¡Aquí tienes tus mejores opciones!"

@app.post("/calcular", response_model=CompraResponse)
async def calcular_compra(request: CompraRequest):
    if not request.productos:
        raise HTTPException(400, "Agrega al menos un producto")

    print(f"Usuario en {request.distrito_usuario} | Presupuesto: S/{request.presupuesto}")

    productos_lista = [
        {"nombre": p.nombre, "cantidad": p.cantidad or 1.0}
        for p in request.productos
    ]

    mejores = calcular_mejores_tiendas(
        productos=productos_lista,
        presupuesto=request.presupuesto,
        df=df_precios
    )

    if not mejores:
        raise HTTPException(404, "No hay tiendas que cumplan con tu presupuesto")

    top3 = mejores[:3]
    nombres_top3 = [t["nombre_tienda"] for t in top3]

    tienda_cercana = kruskal_tienda_mas_cercana(
        distrito_usuario=request.distrito_usuario,
        tiendas_candidatas=nombres_top3
    )

    return CompraResponse(
        mejores_tiendas=[
            TiendaResultado(
                nombre_tienda=t["nombre_tienda"],
                distrito=t["distrito"],
                precio_total=t["precio_total"],
                ahorro=t["ahorro"]
            ) for t in top3
        ],
        tienda_mas_cercana=tienda_cercana,
        precio_mas_bajo=top3[0]["precio_total"]
    )

@app.get("/")
async def root():
    return {"message": "¡Backend Mi Mercadito Pe funcionando al 100%!"}