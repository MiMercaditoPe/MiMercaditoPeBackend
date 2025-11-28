# algoritmos/algoritmo_rutas_mst.py

# Distancias aproximadas entre distritos (puedes ampliar después)
distancias = {
    "Miraflores": {"Barranco": 3, "San Isidro": 5, "Surco": 7, "Surquillo": 4},
    "Barranco": {"Miraflores": 3, "Chorrillos": 6},
    "San Isidro": {"Miraflores": 5, "Lince": 4},
    "Surco": {"Miraflores": 7, "La Molina": 10},
    "Callao": {"San Miguel": 8},
    "San Miguel": {"Callao": 8},
    "Lince": {"San Isidro": 4, "Jesús María": 3},
}

def kruskal_tienda_mas_cercana(distrito_usuario: str, tiendas_candidatas: list):
    """
    Devuelve la tienda más cercana al distrito del usuario
    """
    if not tiendas_candidatas:
        return "Ninguna tienda disponible"
    
    distancia_min = float('inf')
    tienda_ganadora = tiendas_candidatas[0]
    
    for tienda in tiendas_candidatas:
        # Extraer posible distrito del nombre de la tienda (ej: "Metro Miraflores" → Miraflores)
        palabras = tienda.split()
        distrito_tienda = palabras[-1] if len(palabras) > 1 else palabras[0]
        
        if distrito_usuario in distancias and distrito_tienda in distancias[distrito_usuario]:
            dist = distancias[distrito_usuario][distrito_tienda]
            if dist < distancia_min:
                distancia_min = dist
                tienda_ganadora = tienda
    
    return tienda_ganadora