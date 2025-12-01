# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from optimizador import obtener_mejores_tiendas_db
from grafo_distritos import distancia_entre_distritos

app = FastAPI(title="Mi Mercadito Pe - Backend PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    distancia_km: float = 0.0

class CompraResponse(BaseModel):
    mejores_tiendas: List[TiendaResultado]
    tienda_mas_cercana: str
    precio_mas_bajo: float
    mensaje: str = "¡Aquí tienes las mejores opciones!"

@app.post("/calcular", response_model=CompraResponse)
async def calcular_compra(request: CompraRequest):
    if not request.productos:
        raise HTTPException(400, "Agrega al menos un producto")

    productos_lista = [
        {"nombre": p.nombre.strip(), "cantidad": p.cantidad or 1.0}
        for p in request.productos
    ]

    mejores = obtener_mejores_tiendas_db(
        productos=productos_lista,
        presupuesto=request.presupuesto,
        distrito_usuario=request.distrito_usuario
    )

    if not mejores:
        raise HTTPException(404, "No hay tiendas que cumplan con tu presupuesto")

    top3 = mejores[:3]
    nombres_top3 = [t["nombre_tienda"] for t in top3]

    # Tienda más cercana entre las top 3
    tienda_cercana = min(top3, key=lambda t: t["distancia_km"])["nombre_tienda"]

    return CompraResponse(
        mejores_tiendas=[
            TiendaResultado(
                nombre_tienda=t["nombre_tienda"],
                distrito=t["distrito"],
                precio_total=t["precio_total"],
                ahorro=t["ahorro"],
                distancia_km=t["distancia_km"]
            ) for t in top3
        ],
        tienda_mas_cercana=tienda_cercana,
        precio_mas_bajo=top3[0]["precio_total"],
        mensaje="¡Calculado con inteligencia geográfica y precios reales!"
    )

productos = [
    {"nombre": "Arroz costeño 5kg", "cantidad": 1},
    {"nombre": "Aceite primor 1lt", "cantidad": 2},
    {"nombre": "Leche gloria bolsa", "cantidad": 3}
]

resultado = obtener_mejores_tiendas_db(productos, 300.0, "Miraflores")
print(resultado)

@app.get("/")
async def root():
    return {"message": "Mi Mercadito Pe - Backend PRO con Azure SQL + Dijkstra + Backtracking"}