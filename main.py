# algoritmos/algoritmo_backtracking.py
import pandas as pd

def calcular_mejores_tiendas(productos: list, presupuesto: float, df: pd.DataFrame):
    """
    Encuentra tiendas que tengan TODOS los productos y cuyo precio total sea <= presupuesto
    """
    if not productos or presupuesto <= 0:
        return []

    # Normalizar nombres de productos
    productos_lower = [p.lower().strip() for p in productos]
    
    # Filtrar solo las filas que coincidan con alguno de los productos buscados
    mask = df['producto'].str.lower().isin(productos_lower)
    df_filtrado = df[mask].copy()
    
    if df_filtrado.empty:
        return []

    # Agrupar por tienda y verificar que tenga TODOS los productos
    resultados = []
    for tienda, grupo in df_filtrado.groupby('tienda'):
        productos_en_tienda = grupo['producto'].str.lower().unique()
        # Verificar que tenga TODOS los productos buscados
        if all(p in productos_en_tienda for p in productos_lower):
            precio_total = grupo['precio'].sum()
            if precio_total <= presupuesto:
                distrito = "Lima"
                if 'distrito' in df.columns:
                    fila_distrito = df[df['tienda'] == tienda]
                    if not fila_distrito.empty:
                        distrito = fila_distrito.iloc[0].get('distrito', 'Lima')
                
                resultados.append({
                    "nombre_tienda": tienda,
                    "distrito": str(distrito),
                    "precio_total": round(float(precio_total), 2),
                    "ahorro": 0.0
                })

    # Ordenar por precio (mejor primero)
    resultados.sort(key=lambda x: x["precio_total"])
    
    # Devolver máximo 10 resultados
    return resultados[:10]