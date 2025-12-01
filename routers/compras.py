from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from algorithms.algoritmo_backtracking import calcular_mejores_tiendas
from algorithms.algoritmo_rutas_mst import kruskal_tienda_mas_cercana

from database import get_db   

router = APIRouter()


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


@router.post("/calcular", response_model=CompraResponse)
async def calcular_compra(
    body: CompraRequest,
    db: Session = Depends(get_db)  
):


    if not body.productos:
        raise HTTPException(400, "Agrega al menos un producto")

    productos_lista = [
        {"nombre": p.nombre, "cantidad": p.cantidad or 1.0}
        for p in body.productos
    ]

    # TODO: aquí adentro llamarás queries SQL en lugar de CSV
    mejores = calcular_mejores_tiendas(
        productos=productos_lista,
        presupuesto=body.presupuesto,
        db=db  
    )

    if not mejores:
        raise HTTPException(404, "No hay tiendas que cumplan con tu presupuesto")

    top3 = mejores[:3]
    nombres_top3 = [t["nombre_tienda"] for t in top3]

    tienda_cercana = kruskal_tienda_mas_cercana(
        distrito_usuario=body.distrito_usuario,
        tiendas_candidatas=nombres_top3
    )

    return CompraResponse(
        mejores_tiendas=[
            TiendaResultado(
                nombre_tienda=t["nombre_tienda"],
                distrito=t["distrito"],
                precio_total=t["precio_total"],
                ahorro=t["ahorro"],
            ) for t in top3
        ],
        tienda_mas_cercana=tienda_cercana,
        precio_mas_bajo=top3[0]["precio_total"]
    )
