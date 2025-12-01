# grafo_distritos.py
from collections import defaultdict
import heapq

# Aristas reales aproximadas (km por carretera) - COMPLETADO Y CORREGIDO
grafo_aristas = [
    (2, "Miraflores", "Barranco"), (2, "Barranco", "Miraflores"),
    (2, "Miraflores", "Surquillo"), (2, "Surquillo", "Miraflores"),
    (3, "Miraflores", "San Isidro"), (3, "San Isidro", "Miraflores"),
    (4, "San Isidro", "Lince"), (4, "Lince", "San Isidro"),
    (3, "Lince", "Jesús María"), (3, "Jesús María", "Lince"),
    (3, "Jesús María", "San Miguel"), (3, "San Miguel", "Jesús María"),
    (4, "Pueblo Libre", "Jesús María"), (4, "Jesús María", "Pueblo Libre"),
    (3, "San Isidro", "San Borja"), (3, "San Borja", "San Isidro"),
    (4, "San Borja", "Surquillo"), (4, "Surquillo", "San Borja"),
    (4, "San Borja", "Santiago de Surco"), (4, "Santiago de Surco", "San Borja"),
    (5, "Santiago de Surco", "La Molina"), (5, "La Molina", "Santiago de Surco"),
    (5, "Barranco", "Chorrillos"), (5, "Chorrillos", "Barranco"),
    (7, "Chorrillos", "Santiago de Surco"), (7, "Santiago de Surco", "Chorrillos"),
    (9, "Santiago de Surco", "Villa El Salvador"), (9, "Villa El Salvador", "Santiago de Surco"),
    (8, "San Miguel", "Callao"), (8, "Callao", "San Miguel"),
    (5, "Jesús María", "San Martín de Porres"), (5, "San Martín de Porres", "Jesús María"),
    (6, "San Martín de Porres", "Comas"), (6, "Comas", "San Martín de Porres"),
    (12, "Comas", "San Juan de Lurigancho"), (12, "San Juan de Lurigancho", "Comas"),
    (6, "Miraflores", "San Borja"), (6, "San Borja", "Miraflores"),
    (7, "Miraflores", "Santiago de Surco"), (7, "Santiago de Surco", "Miraflores"),
    # Conexiones extra para que no haya distritos aislados
    (10, "San Juan de Lurigancho", "Surquillo"),
]

# Normalización robusta
NORMALIZACION = {
    "surco": "Santiago de Surco",
    "santiago de surco": "Santiago de Surco",
    "san martin de porres": "San Martín de Porres",
    "san martín de porres": "San Martín de Porres",
    "jesus maria": "Jesús María",
    "jesús maría": "Jesús María",
    "villa el salvador": "Villa El Salvador",
}

def normalizar_distrito(distrito: str) -> str:
    if not distrito:
        return "Miraflores"  # fallback
    clave = distrito.strip().lower()
    return NORMALIZACION.get(clave, distrito.strip().title())

# Construcción del grafo (solo una vez)
grafo = defaultdict(dict)
for distancia, a, b in grafo_aristas:
    a_norm = normalizar_distrito(a)
    b_norm = normalizar_distrito(b)
    grafo[a_norm][b_norm] = distancia
    grafo[b_norm][a_norm] = distancia

def distancia_entre_distritos(origen: str, destino: str) -> float:
    """Devuelve distancia en km. Si no hay camino → 999"""
    origen = normalizar_distrito(origen)
    destino = normalizar_distrito(destino)
    
    if origen == destino:
        return 0.0
    
    if origen not in grafo or destino not in grafo:
        return 999.0
    
    # Dijkstra manual
    cola = [(0, origen)]
    visitados = set()
    
    while cola:
        costo, actual = heapq.heappop(cola)
        if actual in visitados:
            continue
        visitados.add(actual)
        
        if actual == destino:
            return round(costo, 1)
            
        for vecino, peso in grafo[actual].items():
            if vecino not in visitados:
                heapq.heappush(cola, (costo + peso, vecino))
    
    return 999.0  # no conectado