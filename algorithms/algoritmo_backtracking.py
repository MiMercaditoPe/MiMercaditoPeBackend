# algoritmos/algoritmo_backtracking.py
import pandas as pd

def calcular_mejores_tiendas(productos: list, presupuesto: float, df: pd.DataFrame):
    if not productos or presupuesto <= 0:
        return []

    resultados = []
    
    # Crear diccionario: producto -> cantidad deseada
    productos_dict = {}
    for p in productos:
        nombre = p["nombre"].strip().lower()
        try:
            cantidad = float(p.get("cantidad", 1))
        except:
            cantidad = 1
        productos_dict[nombre] = cantidad

    productos_buscados = list(productos_dict.keys())

    # Filtrar productos relevantes
    mask = df['producto'].str.lower().isin(productos_buscados)
    df_filtrado = df[mask].copy()

    if df_filtrado.empty:
        return []

    for tienda, grupo in df_filtrado.groupby('tienda'):
        productos_en_tienda = grupo['producto'].str.lower().unique()
        
        # Verificar que tenga TODOS los productos
        if not all(p in productos_en_tienda for p in productos_buscados):
            continue

        precio_total = 0.0
        detalle = []

        for _, fila in grupo.iterrows():
            nombre_prod = fila['producto'].lower().strip()
            precio_unitario = float(fila['precio'])
            cantidad_deseada = productos_dict.get(nombre_prod, 1)
            precio_total += precio_unitario * cantidad_deseada
            detalle.append(f"{fila['producto']} x{cantidad_deseada} = S/{precio_unitario * cantidad_deseada:.2f}")

        if precio_total <= presupuesto:
            distrito = grupo.iloc[0].get('distrito', 'Lima')
            resultados.append({
                "nombre_tienda": tienda,
                "distrito": str(distrito),
                "precio_total": round(precio_total, 2),
                "detalle": detalle,
                "ahorro": 0.0
            })

    resultados.sort(key=lambda x: x["precio_total"])
    return resultados[:10]