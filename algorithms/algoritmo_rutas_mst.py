from .grafo_distritos import GRAFOS_DISTANCIAS

def kruskal_tienda_mas_cercana(distrito_usuario, tiendas_candidatas):
    """
    Selecciona la tienda más cercana usando distancias del grafo.

    distrito_usuario: str
    tiendas_candidatas: lista de nombres de tienda

    El grafo debe tener esta forma en grafo_distritos.py:
    GRAFOS_DISTANCIAS = {
        ("San Miguel", "Magdalena"): 5,
        ("San Miguel", "Pueblo Libre"): 7,
        ...
    }
    """

    mejores_opciones = []
    for tienda in tiendas_candidatas:
        for (a, b), distancia in GRAFOS_DISTANCIAS.items():
            if a == distrito_usuario and b == tienda:
                mejores_opciones.append((tienda, distancia))
            if b == distrito_usuario and a == tienda:
                mejores_opciones.append((tienda, distancia))

    if not mejores_opciones:
        return tiendas_candidatas[0]

    mejores_opciones.sort(key=lambda x: x[1])

    return mejores_opciones[0][0]
