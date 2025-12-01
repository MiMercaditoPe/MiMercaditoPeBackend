import pandas as pd

def calcular_mejores_tiendas(productos, presupuesto, df):
    """
    productos: lista de {nombre, cantidad}
    presupuesto: número
    df: dataset completo con columnas:
        - tienda
        - producto
        - precio
        - distrito
    """

    resultados = []

    tiendas = df["tienda"].unique()

    for tienda in tiendas:
        subtotal = 0
        disponible = True
        distrito = df[df["tienda"] == tienda]["distrito"].iloc[0]

        for item in productos:
            nombre = item["nombre"]
            cantidad = item["cantidad"]

            fila = df[(df["tienda"] == tienda) & (df["producto"] == nombre)]

            if fila.empty:
                disponible = False
                break

            precio_unit = float(fila["precio"].iloc[0])
            subtotal += precio_unit * cantidad

        if not disponible:
            continue

        if subtotal <= presupuesto:
            resultados.append({
                "nombre_tienda": tienda,
                "distrito": distrito,
                "precio_total": subtotal,
                "ahorro": presupuesto - subtotal
            })

    resultados = sorted(resultados, key=lambda x: x["precio_total"])

    return resultados
