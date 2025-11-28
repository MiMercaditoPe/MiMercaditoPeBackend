# algoritmos/algoritmo_backtracking.py
import pandas as pd

def calcular_mejores_tiendas(productos: list, presupuesto: float, df: pd.DataFrame):
    """
    Recibe lista de nombres de productos (en minúscula) y presupuesto
    Devuelve lista ordenada de tiendas con precio_total (de menor a mayor)
    """
    productos = [p.lower().strip() for p in productos]
    
    # Filtrar productos que existen en el dataset
    filas_relevantes = df[df['producto'].str.lower().isin(productos)]
    
    if filas_relevantes.empty:
        return []

    # Agrupar por tienda y sumar precios
    resultado = []
    for tienda, grupo in filas_relevantes.groupby('tienda'):
        precio_total = grupo['precio'].sum()
        if precio_total <= presupuesto:
            # Buscar distrito de la tienda
            distrito = df[df['tienda'] == tienda]['distrito'].iloc[0] if not df[df['tienda'] == tienda]['distrito'].empty else "Lima"
            resultado.append({
                "nombre_tienda": tienda,
                "distrito": distrito,
                "precio_total": precio_total,
                "ahorro": 0  # puedes calcularlo después si quieres
            })
    
    # Ordenar por precio
    resultado.sort(key=lambda x: x["precio_total"])
    return resultado