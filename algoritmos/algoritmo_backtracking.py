# algoritmos/algoritmo_backtracking.py
import pandas as pd

def calcular_mejores_tiendas(productos: list, presupuesto: float, df: pd.DataFrame):
    """
    Fuerza bruta simple: agrupa por tienda y suma precios
    """
    productos_lower = [p.lower().strip() for p in productos]
    
    # Filtrar filas que tengan alguno de los productos buscados
    mask = df['producto'].str.lower().isin(productos_lower)
    df_filtrado = df[mask].copy()
    
    if df_filtrado.empty:
        return []

    # Agrupar por tienda y sumar precios
    tiendas = []
    for tienda, grupo in df_filtrado.groupby('tienda'):
        precio_total = grupo['precio'].sum()
        if precio_total <= presupuesto:
            # Intentar obtener distrito (ajusta la columna si tu CSV tiene otro nombre)
            distrito = "Lima"
            if 'distrito' in df.columns:
                distrito_row = df[df['tienda'] == tienda]['distrito']
                if not distrito_row.empty:
                    distrito = distrito_row.iloc[0]
            
            tiendas.append