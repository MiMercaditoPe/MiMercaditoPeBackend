# algoritmos/algoritmo_rutas_mst.py
from grafo_distritos import distancia_entre_distritos

def obtener_distrito_tienda(nombre_tienda: str) -> str:
    partes = nombre_tienda.split()
    if len(partes) >= 2:
        posible = partes[-1]
        if posible in ["Miraflores", "Barranco", "Surco", "Callao", "Lince"]:
            return posible
        if posible == "Surco":
            return "Santiago de Surco"
    return "Lima"  # fallback

def kruskal_tienda_mas_cercana(distrito_usuario: str, tiendas_candidatas: list):
    if not tiendas_candidatas:
        return "Ninguna disponible"
    
    mejor_tienda = None
    menor_distancia = float('inf')
    
    distrito_usuario = distrito_usuario.strip()
    
    for tienda in tiendas_candidatas:
        distrito_tienda = obtener_distrito_tienda(tienda)
        dist = distancia_entre_distritos(distrito_usuario, distrito_tienda)
        
        if dist < menor_distancia:
            menor_distancia = dist
            mejor_tienda = tienda
    
    return mejor_tienda or tiendas_candidatas[0]