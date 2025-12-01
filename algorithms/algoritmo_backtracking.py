# algoritmo_backtracking.py
from sqlalchemy import text
from sqlalchemy.orm import Session

def calcular_mejores_tiendas(productos, presupuesto, db: Session):
    """
    productos: lista de {nombre, cantidad}
    presupuesto: número
    db: sesión SQLAlchemy
    """

    resultados = []

    # Obtener todas las tiendas (usando text para SQL crudo)
    sql_tiendas = text("SELECT DISTINCT tienda FROM PRECIOS")
    res = db.execute(sql_tiendas)
    # res.scalars() devuelve los valores de la primera columna si la consulta lo permite
    tiendas = [row[0] for row in res.fetchall()]

    for tienda in tiendas:

        # Obtener distrito de la tienda (TOP 1 es válido para SQL Server)
        sql_distrito = text("SELECT TOP 1 distrito FROM PRECIOS WHERE tienda = :t")
        distrito_row = db.execute(sql_distrito, {"t": tienda}).fetchone()

        if not distrito_row:
            continue

        distrito = distrito_row[0]

        subtotal = 0
        disponible = True

        # Revisar cada producto requerido
        for item in productos:
            nombre = item["nombre"]

            sql_precio = text("""
                SELECT precio FROM PRECIOS
                WHERE tienda = :t AND producto = :p
            """)
            fila = db.execute(sql_precio, {"t": tienda, "p": nombre}).fetchone()

            if not fila:
                disponible = False
                break

            precio_unit = float(fila[0])
            subtotal += precio_unit

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
