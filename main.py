from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd

# ← AQUÍ IMPORTA TUS ALGORITMOS (asegúrate que existan estas carpetas/archivos)
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

# ===================== CARGA DE DATOS =====================
print("Cargando datos desde la carpeta data/ ...")
df_precios = pd.read_csv("data/dataset_compras_completo.csv", encoding="utf-8")
# df_precios = pd.read_csv("data/dataset_compras_completo_cleaned.csv", encoding="utf-8")
df_tiendas = pd.read_csv("data/tiendas.csv", encoding="utf-8")
print(f"Datos cargados: {len(df_precios)} filas de precios, {len(df_tiendas)} tiendas")

# ===================== MODELOS =====================
class ProductoInput(BaseModel):
    nombre: str
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

# ===================== RUTA =====================
@app.post("/calcular", response_model=CompraResponse)
async def calcular_compra(request: CompraRequest):
    if not request.productos:
        raise HTTPException(400, detail="Debes agregar al menos un producto")

    nombres_productos = [p.nombre.strip().lower() for p in request.productos]

    print(f"Calculando para: {request.distrito_usuario} | Presupuesto: S/ {request.presupuesto}")
    print(f"Productos: {nombres_productos}")

    mejores = calcular_mejores_tiendas(
        productos=nombres_productos,
        presupuesto=request.presupuesto,
        df=df_precios
    )

    if not mejores:
        raise HTTPException(404, detail="No hay tiendas dentro del presupuesto")

    top3 = mejores[:3]
    nombres_top3 = [t["nombre_tienda"] for t in top3]

    tienda_cercana = kruskal_tienda_mas_cercana(
        distrito_usuario=request.distrito_usuario,
        tiendas_candidatas=nombres_top3
    )

    respuesta = CompraResponse(
        mejores_tiendas=[
            TiendaResultado(
                nombre_tienda=t["nombre_tienda"],
                distrito=t.get("distrito", "Lima"),
                precio_total=round(t["precio_total"], 2),
                ahorro=round(t.get("ahorro", 0), 2)
            ) for t in top3
        ],
        tienda_mas_cercana=tienda_cercana,
        precio_mas_bajo=round(top3[0]["precio_total"], 2)
    )

    return respuesta

@app.get("/")
async def root():
    return {"message": "¡Backend Mi Mercadito Pe funcionando al 100%!"}